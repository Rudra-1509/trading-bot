import unittest
from types import SimpleNamespace

from bot.orders import BinanceOrder
from bot.validators import Validator


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.client = SimpleNamespace(valid_symbols=["BTCUSDT", "ETHUSDT"])
        self.validator = Validator(self.client)

    def test_validate_accepts_valid_market_order(self):
        payload = self.validator.validate("btcusdt", "buy", "market", 0.01, None)

        self.assertEqual(payload["symbol"], "BTCUSDT")
        self.assertEqual(payload["side"], "BUY")
        self.assertEqual(payload["order_type"], "MARKET")
        self.assertEqual(payload["quantity"], 0.01)
        self.assertIsNone(payload["price"])

    def test_validate_rejects_invalid_symbol(self):
        with self.assertRaisesRegex(ValueError, "Invalid trading symbol"):
            self.validator.validate("badcoin", "buy", "market", 0.01)

    def test_validate_rejects_limit_order_without_price(self):
        with self.assertRaisesRegex(ValueError, "LIMIT orders require a price"):
            self.validator.validate("BTCUSDT", "buy", "limit", 0.01, None)

    def test_format_response_extracts_key_fields(self):
        order = {
            "orderId": 12345,
            "symbol": "BTCUSDT",
            "side": "BUY",
            "status": "FILLED",
            "type": "MARKET",
            "executedQty": "0.010000",
            "avgPrice": "50000.00",
            "transactTime": 1710000000000,
        }

        formatter = BinanceOrder(client=None)
        formatted = formatter.format_response(order)

        self.assertEqual(formatted["orderId"], 12345)
        self.assertEqual(formatted["symbol"], "BTCUSDT")
        self.assertEqual(formatted["status"], "FILLED")
        self.assertEqual(formatted["avgPrice"], "50000.00")


if __name__ == "__main__":
    unittest.main(verbosity=2)
