import logging
from typing import Optional


class BinanceOrder:
    def __init__(self,client):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def execute_order(
        self,
        symbol: str,
        side: str = None,
        order_type: str = None,
        quantity: float = None,
        price: Optional[float] = None,
    ):
        """
        Decide which order type to execute.
        """

        try:
            self.logger.info(
                f"Executing {order_type} order | "
                f"Symbol={symbol}, Side={side}, Qty={quantity}, Price={price}"
            )

            if order_type == "MARKET":
                order = self.client.place_market_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                )

            elif order_type == "LIMIT":
                order = self.client.place_limit_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    price=price,
                )

            else:
                raise ValueError(f"Unsupported order type: {order_type}")

            if order is None:
                raise RuntimeError("Order placement returned None.")

            self.logger.info(
                f"Order executed successfully | "
                f"OrderID={order['orderId']} | "
                f"Status={order['status']}"
            )


            return order

        except Exception as e:
            self.logger.error(f"Failed to execute order: {e}")
            raise

    def format_response(self, order: dict) -> dict:
        """
        Extract only the important fields from the Binance response.
        """

        return {
            "orderId": order.get("orderId"),
            "symbol": order.get("symbol"),
            "side": order.get("side"),
            "status": order.get("status"),
            "type": order.get("type"),
            "executedQty": order.get("executedQty"),
            "avgPrice": order.get("avgPrice", "N/A"),
            "transactTime": order.get("transactTime"),
        }

    def print_summary(self, order_response: dict):
        """
        Print a clean order summary.
        """

        print("\n========== ORDER SUMMARY ==========")
        print(f"Order ID          : {order_response['orderId']}")
        print(f"Symbol            : {order_response['symbol']}")
        print(f"Side              : {order_response['side']}")
        print(f"Type              : {order_response['type']}")
        print(f"Status            : {order_response['status']}")
        print(f"Executed Qty      : {order_response['executedQty']}")
        print(f"Average Price     : {order_response['avgPrice']}")
        print(f"Transaction Time  : {order_response['transactTime']}")
        print("===================================\n")

        self.logger.info("Order summary displayed.")