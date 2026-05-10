# 🤖 Binance Futures Testnet Trading Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python\&logoColor=white)](https://python.org)
[![python-binance](https://img.shields.io/badge/python--binance-orange)](https://python-binance.readthedocs.io/)
[![Rich CLI](https://img.shields.io/badge/Rich-CLI-purple)](https://github.com/Textualize/rich)
[![Binance Futures Testnet](https://img.shields.io/badge/Binance-Futures%20Testnet-yellow)](https://testnet.binancefuture.com)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-brightgreen)](https://pep8.org)

> A production-style Python CLI trading bot for placing MARKET and LIMIT orders on Binance Futures Testnet (USDT-M) with modular architecture, structured logging, validation, and professional terminal UI.

---

# 📌 Overview

This project is a modular Python command-line trading bot built for the Binance Futures Testnet.

The application demonstrates real-world backend engineering practices including:

* layered architecture,
* reusable service modules,
* structured logging,
* defensive input validation,
* exception handling,
* and clean terminal UX.

The bot supports:

* MARKET orders,
* LIMIT orders,
* BUY / SELL operations,
* interactive CLI workflows,
* and detailed request/response logging.

The project is designed for:

* backend engineering practice,
* API integration workflows,
* CLI application development,
* and trading system fundamentals.

---

# 🚀 Features

| Feature                 | Description                                    |
| ----------------------- | ---------------------------------------------- |
| MARKET Orders           | Execute market buy/sell orders                 |
| LIMIT Orders            | Place target-price limit orders                |
| BUY / SELL Support      | Supports both trading sides                    |
| Input Validation        | Prevents invalid API requests                  |
| Structured Logging      | Logs API requests, responses, and failures     |
| Rich CLI Interface      | Professional terminal UI using `rich`          |
| Interactive Mode        | Prompt-based guided order flow                 |
| Confirmation Prompt     | Prevents accidental order execution            |
| Error Handling          | Handles API and validation failures gracefully |
| Modular Architecture    | Clean separation of concerns                   |
| Binance Futures Testnet | Safe paper-trading environment                 |

---

# 🛠 Tech Stack

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python 3.x     | Core programming language       |
| python-binance | Binance Futures API integration |
| rich           | Advanced terminal UI            |
| questionary    | Interactive CLI prompts         |
| argparse       | Command-line argument parsing   |
| python-dotenv  | Environment variable management |
| logging        | Structured logging system       |

---

# 🏗 Architecture

```text
User Input
   ↓
CLI Layer
   ↓
Validation Layer
   ↓
Order Service Layer
   ↓
Binance Client Layer
   ↓
Binance Futures Testnet API
```

---

# 📁 Project Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   ├── logging_config.py
│   └── utils.py
│
├── logs/
│   └── trading.log
│
├── .env.example
├── .gitignore
├── cli.py
├── README.md
└── requirements.txt
```

---

# 🌐 Binance Futures Testnet Setup

## 1. Open Binance Futures Testnet

Visit:

https://testnet.binancefuture.com

---

## 2. Login

Login using your GitHub account.

---

## 3. Generate API Keys

1. Open API Management
2. Create a new API Key
3. Copy:

   * API Key
   * Secret Key

---

## 4. Configure `.env`

Create a `.env` file in the project root directory:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret_key
```

⚠️ Never upload your `.env` file to GitHub.

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Prasannaganesann/Binance-Futures-Testnet-Bot.git
cd Binance-Futures-Testnet-Bot
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows CMD

```bash
venv\Scripts\activate
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

| Variable           | Description                        |
| ------------------ | ---------------------------------- |
| BINANCE_API_KEY    | Binance Futures Testnet API Key    |
| BINANCE_API_SECRET | Binance Futures Testnet Secret Key |

---

# 💻 Usage

## MARKET BUY Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

## MARKET SELL Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

---

## LIMIT BUY Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000
```

---

## LIMIT SELL Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 200000
```

---

## Interactive Mode

```bash
python cli.py --interactive
```

---

## Help Menu

```bash
python cli.py --help
```

---

# 📸 Example Output

## MARKET Order

```text
ORDER REQUEST
Symbol      : BTCUSDT
Side        : BUY
Order Type  : MARKET
Quantity    : 0.001

ORDER RESPONSE
Order ID    : 13126020199
Status      : NEW
ExecutedQty : 0.000000

SUCCESS: Order placed successfully.
```

---

## Validation Failure

```text
❌ Quantity must be greater than 0. Got: -1.0
```

---

# 📝 Logging System

All API activity is logged to:

```text
logs/trading.log
```

The logging system records:

* API requests
* API responses
* validation failures
* warnings
* exceptions
* connection status

---

## Example Logs

```text
2026-05-10 14:41:03 | INFO | ORDER REQUEST | symbol=BTCUSDT
2026-05-10 14:41:04 | INFO | ORDER RESPONSE | order_id=13126020199
2026-05-10 14:42:04 | WARNING | Quantity validation failed
```

---

# 🛡 Error Handling

The application handles:

| Error Type          | Handling             |
| ------------------- | -------------------- |
| Invalid quantity    | Validation error     |
| Missing price       | Validation error     |
| Invalid side/type   | Validation error     |
| Missing API key     | Environment error    |
| Binance API failure | Exception handling   |
| Network failure     | Logged and displayed |
| Invalid credentials | Safe error handling  |

---

# 🎁 Bonus Feature

## Interactive Rich CLI Mode

The project includes a guided interactive terminal interface using:

* `rich`
* `questionary`

Features include:

* prompt-based order flow,
* formatted tables,
* colored terminal output,
* confirmation prompts,
* validation feedback,
* and improved CLI usability.

---

# 📌 Assumptions

* Binance Futures Testnet only
* USDT-M futures contracts only
* LIMIT orders use GTC (Good Till Cancelled)
* Single-order execution per CLI invocation

---

# 📚 Future Improvements

Potential future enhancements:

* OCO order support
* TWAP strategy
* Grid trading strategy
* Web dashboard
* Docker deployment
* Unit testing
* CI/CD pipelines
* Async order execution

---

# 🐙 GitHub Repository

Repository:

https://github.com/Prasannaganesann/Binance-Futures-Testnet-Bot

---

# 📄 License

MIT License © 2026 Prasanna Ganesan
