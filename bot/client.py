import os
import logging
from typing import Optional

from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

load_dotenv()


class BinanceClient:
    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        testnet = os.getenv("BINANCE_TESTNET")

        if not api_key or not api_secret:
            raise ValueError("API Key or Secret not found in .env")

        self.client = Client(api_key, api_secret, testnet=testnet)
        
        exchange_info=self.client.futures_exchange_info()
        symbols=[sym["symbol"] for sym in exchange_info["symbols"]]
        self.valid_symbols=symbols
        
        # Configure Futures Testnet
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        self.logger = logging.getLogger(__name__)

    def ping(self):
        """Check if Binance API is reachable."""
        try:
            self.client.ping()
            self.logger.info("Connected to Binance successfully.")
            return True
        except Exception as e:
            self.logger.exception("Ping failed.")
            raise e

    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: Optional[float]
    ):
        """Place a MARKET order."""

        try:
            self.logger.info(f"MARKET Order -> {side} {quantity} {symbol}")

            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity,
            )

            self.logger.info(f"Order placed successfully: {order}")

            return order

        except (BinanceAPIException, BinanceRequestException) as e:
            self.logger.exception("Failed to place MARKET order.")
            raise e

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
    ):
        """Place a LIMIT order."""

        try:
            self.logger.info(f"LIMIT Order -> {side} {quantity} {symbol} @ {price}")

            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC",
            )

            self.logger.info(f"Order placed successfully: {order}")

            return order

        except (BinanceAPIException, BinanceRequestException) as e:
            self.logger.exception("Failed to place LIMIT order.")
            raise e

    def get_order(self, symbol: str, order_id: int):
        """Fetch an existing order."""

        try:
            order = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id,
            )

            return order

        except (BinanceAPIException, BinanceRequestException) as e:
            self.logger.exception("Unable to fetch order.")
            raise e
