import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from bot.client import BinanceClient
from bot.orders import BinanceOrder
from bot.validators import Validator
from bot.logging_config import setup_logging


app = typer.Typer()

console = Console()


@app.command()
def trade():
    """Place a Binance Market or Limit Order."""

    console.print(
        Panel.fit(
            "[bold cyan]🚀 Binance Trading Bot[/bold cyan]\n"
            "[green]Binance Futures Testnet • Interactive CLI[/green]",
            border_style="bright_blue",
        )
    )

    # ---------------- SYMBOL ----------------
    symbol = Prompt.ask("🪙 Enter Trading Symbol")

    # ---------------- SIDE ----------------
    console.print("\n[bold yellow]📌 Choose Order Side[/bold yellow]")
    console.print("🟢 1. BUY")
    console.print("🔴 2. SELL")

    choice = Prompt.ask("Enter choice", choices=["1", "2"])

    side = "BUY" if choice == "1" else "SELL"

    # ---------------- TYPE ----------------
    console.print("\n[bold yellow]📌 Choose Order Type[/bold yellow]")
    console.print("⚡ 1. MARKET")
    console.print("📊 2. LIMIT")

    choice = Prompt.ask("Enter choice", choices=["1", "2"])

    order_type = "MARKET" if choice == "1" else "LIMIT"

    # ---------------- QUANTITY ----------------
    quantity = float(Prompt.ask("📦 Enter Quantity"))

    # ---------------- PRICE ----------------
    price = None
    if order_type == "LIMIT":
        price = float(Prompt.ask("💰 Enter Limit Price"))

    # ---------------- ORDER REVIEW ----------------
    review = Table(title="📋 Order Preview", border_style="cyan")

    review.add_column("Field", style="cyan", justify="left")
    review.add_column("Value", style="green")

    review.add_row("🪙 Symbol", symbol)
    review.add_row("📌 Side", side)
    review.add_row("📈 Type", order_type)
    review.add_row("📦 Quantity", str(quantity))

    if price is not None:
        review.add_row("💰 Price", str(price))

    console.print()
    console.print(review)

    if not Confirm.ask("\n✅ Confirm Order?"):
        console.print("\n[yellow]⚠️ Order Cancelled by User.[/yellow]")
        raise typer.Exit()

    # ---------------- INITIALIZE ----------------
    try:
        setup_logging()
        client = BinanceClient()
        validator = Validator(client)
        orders = BinanceOrder(client)

        with console.status(
            "[bold green]🔄 Validating Order...[/bold green]",
            spinner="dots",
        ):
            validated = validator.validate(
                symbol,
                side,
                order_type,
                quantity,
                price,
            )

        with console.status(
            "[bold green]🚀 Sending Order to Binance...[/bold green]",
            spinner="earth",
        ):
            order = orders.execute_order(validated)

        formatted = orders.format_response(order)

    except Exception as e:
        console.print(
            Panel.fit(
                f"[bold red]❌ Order Failed[/bold red]\n\n{e}",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    # ---------------- SUCCESS ----------------
    console.print()
    console.print(
        Panel.fit(
            "[bold green]🎉 Order Successfully Executed![/bold green]",
            f"[green]Order ID: {str(formatted.get('orderId', '-'))}[/green]",
            border_style="green",
        )
    )

    # ---------------- SUMMARY TABLE ----------------
    table = Table(
        title="📈 Binance Order Summary",
        border_style="bright_green",
        show_lines=True,
    )

    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("🆔 Order ID", str(formatted.get("orderId", "-")))
    table.add_row("🪙 Symbol", formatted.get("symbol", "-"))
    table.add_row("📌 Side", formatted.get("side", "-"))
    table.add_row("📈 Type", formatted.get("type", "-"))
    table.add_row("📊 Status", formatted.get("status", "-"))
    table.add_row("📦 Executed Qty", str(formatted.get("executedQty", "-")))
    table.add_row("💰 Average Price", str(formatted.get("avgPrice", "-")))

    if formatted.get("transactTime"):
        table.add_row("⏰ Time", str(formatted["transactTime"]))

    console.print(table)

    console.print(
        "\n[bold bright_green]✅ Thank you for using Binance CLI Trading Bot![/bold bright_green] 🚀"
    )


if __name__ == "__main__":
    app()
