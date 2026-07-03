import logging
from typing import Optional


class Validator:
    def __init__(self,client):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def validate_symbol(self, symbol: str):
        """Validate trading symbol."""

        normalized_symbol = symbol.upper()

        if normalized_symbol not in self.client.valid_symbols:
            raise ValueError(f"Invalid trading symbol: {symbol}")

        return normalized_symbol

    def validate_order_type(self, order_type: str):
        """Validate order type."""

        order_type = order_type.upper()

        if order_type not in ["MARKET", "LIMIT"]:
            raise ValueError(
                "Order type must be either MARKET or LIMIT."
            )

        return order_type

    def validate_side(self, side: str):
        """Validate BUY/SELL."""

        side = side.upper()

        if side not in ["BUY", "SELL"]:
            raise ValueError(
                "Side must be either BUY or SELL."
            )

        return side

    def validate_quantity(self, quantity: float):
        """Validate quantity."""

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

    def validate_price(
        self,
        order_type: str,
        price: Optional[float],
    ):
        """Validate price for LIMIT orders."""

        if order_type == "LIMIT":

            if price is None:
                raise ValueError(
                    "LIMIT orders require a price."
                )

            if price <= 0:
                raise ValueError(
                    "Price must be greater than zero."
                )

    def validate(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ):
        """
        Validate all user inputs.
        """

        symbol = self.validate_symbol(symbol)

        side = self.validate_side(side)

        order_type = self.validate_order_type(order_type)

        self.validate_quantity(quantity)

        self.validate_price(order_type, price)

        self.logger.info(
            f"Validation successful for {symbol}"
        )

        return {
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "quantity": quantity,
            "price": price,
        }