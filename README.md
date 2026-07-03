# 🚀 Binance Trading Bot – Futures Testnet

A clean, production-ready Python CLI application for placing **Market** and **Limit** orders on Binance Futures Testnet (USDT-M futures). Built with structured architecture, comprehensive logging, and robust error handling.

---

## ✨ Features

- **Market & Limit Orders** – Place both order types on Binance Futures Testnet
- **BUY/SELL Support** – Full support for both trading sides
- **Interactive CLI** – User-friendly prompts with real-time order preview
- **Input Validation** – Symbol, quantity, and price validation before placing orders
- **Structured Code** – Separation of concerns (client layer, order logic, CLI)
- **Comprehensive Logging** – File-based logging to track all API interactions and errors
- **Error Handling** – Graceful exception handling for API failures, invalid inputs, and network issues
- **Order Summary** – Detailed response formatting with execution details

---

## 🛠️ Prerequisites

### System Requirements
- Python 3.8+
- pip (Python package manager)

### Binance Testnet Account
1. Register at [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Complete account activation
3. Generate API credentials:
   - API Key
   - API Secret
4. **Important:** Use testnet credentials, NOT live trading keys

---

## 📦 Installation

### 1. Clone or Download the Repository
```bash
git clone <your-repo-url>
cd trading-bot
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
BINANCE_TESTNET=True
```

**⚠️ Security:** Never commit `.env` to version control. Add it to `.gitignore`.

---

## 🚀 Usage

### Run the Trading Bot CLI
```bash
python cli.py
```

### Interactive Workflow

1. **Enter Trading Symbol**  
   Example: `BTCUSDT`, `ETHUSDT`

2. **Choose Order Side**  
   - 🟢 BUY (buy crypto)
   - 🔴 SELL (sell crypto)

3. **Select Order Type**  
   - ⚡ MARKET (execute immediately at market price)
   - 📊 LIMIT (execute at a specific price)

4. **Enter Quantity**  
   Example: `0.01`

5. **Enter Price (for LIMIT orders only)**  
   Example: `45000.00`

6. **Review & Confirm**  
   A summary table shows order details. Confirm to place the order.

7. **View Results**  
   Success screen displays Order ID, Status, Executed Quantity, and Average Price.

### Example Commands
```bash
# Run the CLI
python cli.py

# The app will guide you through an interactive prompt:
# 🪙 Enter Trading Symbol: BTCUSDT
# 📌 Choose Order Side: 1 (BUY)
# 📌 Choose Order Type: 1 (MARKET)
# 📦 Enter Quantity: 0.01
# ✅ Confirm Order? [y/n]: y
```

---

## 📁 Project Structure

```
trading-bot/
├── bot/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance API client wrapper
│   ├── orders.py                # Order placement & formatting logic
│   ├── validators.py            # Input validation
│   └── logging_config.py        # Logging configuration
├── logs/
│   └── trading.log              # Application logs
├── cli.py                       # CLI entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

### Module Overview

**`bot/client.py`**
- Wrapper around `python-binance` library
- Handles authentication and API calls
- Methods: `place_market_order()`, `place_limit_order()`, `get_order()`

**`bot/orders.py`**
- Order execution logic
- Routes market/limit orders to appropriate client methods
- Formats API responses for CLI display

**`bot/validators.py`**
- Validates user inputs (symbol, side, quantity, price)
- Normalizes inputs (uppercase conversion, range checks)
- Raises descriptive errors for invalid inputs

**`bot/logging_config.py`**
- Centralized logging setup
- Logs to both file (`logs/trading.log`) and console
- Format: `timestamp | level | module | message`

**`cli.py`**
- CLI entry point using Typer framework
- Interactive prompts with Rich formatting
- Order preview table before confirmation

---

## 📋 Logging

All API interactions and errors are logged to `logs/trading.log`:

```
2024-01-15 10:30:45,123 | INFO | bot.client | Connected to Binance successfully.
2024-01-15 10:30:46,456 | INFO | bot.orders | Executing MARKET order | Symbol=BTCUSDT, Side=BUY, Qty=0.01, Price=None
2024-01-15 10:30:47,789 | INFO | bot.client | Order placed successfully: {...}
```

### Log Levels
- **INFO** – Successful operations
- **WARNING** – Potential issues
- **ERROR** – Failed operations
- **EXCEPTION** – Stack traces for debugging

---

## ✅ Input Validation

The bot validates all user inputs:

| Field | Rules |
|-------|-------|
| **Symbol** | Must exist on Binance Futures (e.g., BTCUSDT) |
| **Side** | Must be BUY or SELL |
| **Order Type** | Must be MARKET or LIMIT |
| **Quantity** | Must be > 0 |
| **Price (LIMIT)** | Must be > 0; required for LIMIT orders |

**Example Error Messages:**
```
❌ Invalid trading symbol: INVALIDUSDT
❌ Quantity must be greater than zero.
❌ LIMIT orders require a price.
```

---

## ⚠️ Error Handling

The bot handles common errors gracefully:

| Error | Action |
|-------|--------|
| Invalid symbol | Rejects with clear message |
| Network failure | Catches connection errors and logs |
| API errors | Displays Binance error message |
| Missing credentials | Raises error at startup with helpful message |
| Invalid quantity/price | Prompts to re-enter |

All exceptions are logged with full stack traces to help debugging.

---

## 🧪 Testing

Run validation tests:
```bash
python -m unittest discover -s tests -v
```

Run syntax check:
```bash
python -m py_compile cli.py bot/*.py
```

---

## 📝 Sample Output

### Successful Order
```
🚀 Binance Trading Bot
Binance Futures Testnet • Interactive CLI

📋 Order Preview
┌──────────────┬──────────┐
│ Field        │ Value    │
├──────────────┼──────────┤
│ 🪙 Symbol    │ BTCUSDT  │
│ 📌 Side      │ BUY      │
│ 📈 Type      │ MARKET   │
│ 📦 Quantity  │ 0.01     │
└──────────────┴──────────┘

✅ Confirm Order? [y/n]: y

🎉 Order Successfully Executed!
Order ID: 123456789

📈 Binance Order Summary
┌──────────────────┬──────────────┐
│ 🆔 Order ID      │ 123456789    │
│ 🪙 Symbol        │ BTCUSDT      │
│ 📌 Side          │ BUY          │
│ 📈 Type          │ MARKET       │
│ 📊 Status        │ FILLED       │
│ 📦 Executed Qty  │ 0.01         │
│ 💰 Average Price │ 45000.50     │
└──────────────────┴──────────────┘

✅ Thank you for using Binance CLI Trading Bot! 🚀
```

### Failed Order
```
❌ Order Failed

Invalid trading symbol: INVALID
```

---

## 🔐 Security Best Practices

1. **Never share API credentials** – Keep `.env` file private
2. **Use testnet credentials** – Never use live trading keys
3. **Limit API permissions** – Only enable "Futures" and "Place orders"
4. **Rotate credentials regularly** – Regenerate keys periodically
5. **Monitor logs** – Review `logs/trading.log` for suspicious activity

---

## 📚 Dependencies

| Package | Purpose |
|---------|---------|
| `typer` | CLI framework with rich formatting |
| `rich` | Beautiful terminal output |
| `requests` | HTTP library |
| `python-binance` | Binance API client |
| `python-dotenv` | Environment variable loading |

See `requirements.txt` for versions.

---

## 🐛 Troubleshooting

### "API Key or Secret not found in .env"
- Ensure `.env` file exists in project root
- Check keys are spelled correctly: `BINANCE_API_KEY`, `BINANCE_API_SECRET`
- Restart your terminal to reload environment variables

### "Invalid trading symbol: BTCUSDT"
- Verify the symbol is supported on Binance Futures
- Check spelling (symbols are case-insensitive, e.g., `btcusdt` works)
- Common symbols: BTCUSDT, ETHUSDT, BNBUSDT

### "Connection refused" / Timeout
- Check your internet connection
- Verify Binance API is accessible: https://testnet.binancefuture.com
- Review logs in `logs/trading.log`

### "Order rejected by API"
- Insufficient balance for the order
- Quantity below minimum lot size
- Price outside acceptable range
- Check Binance error message in output

---

## 📖 Assumptions & Limitations

### Assumptions
- Binance Futures Testnet is accessible
- User has valid testnet credentials with "Futures" and "Trade" permissions
- Trading pairs exist on testnet (BTCUSDT, ETHUSDT, etc.)
- User understands basic trading concepts (Market/Limit, BUY/SELL)

### Limitations
- **Testnet only** – Not for live trading
- **Basic order types** – Only MARKET and LIMIT orders
- **No order management** – Cannot modify or cancel orders through this CLI
- **No portfolio view** – Cannot check balance or open positions
- **Single order** – Places one order at a time

### Future Enhancements
- ✅ Stop-Loss / Take-Profit orders
- ✅ Batch order placement
- ✅ Portfolio dashboard
- ✅ Order history and analytics
- ✅ Web UI

---

## 🤝 Contributing

Found a bug or want to add a feature? Open an issue or submit a pull request!

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in `logs/trading.log`
3. Verify `.env` configuration
4. Check Binance API documentation: https://binance-docs.github.io/apidocs/

---

## 📜 License

This project is provided as-is for educational and evaluation purposes.

---

## 🎯 Quick Start Checklist

- [ ] Set up Binance Futures Testnet account
- [ ] Generate API credentials
- [ ] Clone repository
- [ ] Create `.env` file with credentials
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run: `python cli.py`
- [ ] Place a test order
- [ ] Check `logs/trading.log` for successful log entries

---

**Happy trading! 🚀**
