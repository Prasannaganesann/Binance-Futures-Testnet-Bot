# 🤖 Binance Futures Testnet Trading Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![python-binance](https://img.shields.io/badge/python--binance-1.0.19-orange)](https://python-binance.readthedocs.io/)
[![Rich](https://img.shields.io/badge/Rich-CLI-purple)](https://github.com/Textualize/rich)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Testnet](https://img.shields.io/badge/Binance-Futures%20Testnet-yellow)](https://testnet.binancefuture.com)
[![Code Style: PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen)](https://pep8.org)

> A clean, modular, production-quality Python CLI application for placing **MARKET** and **LIMIT** futures orders on the **Binance Futures Testnet** (USDT-M).

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Binance Testnet Setup](#binance-testnet-setup)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Example Outputs](#example-outputs)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [Bonus Feature](#bonus-feature)
- [Assumptions](#assumptions)
- [GitHub Strategy](#github-strategy)

---

## 🔍 Project Overview

This trading bot connects to the **Binance Futures Testnet** and allows users to place MARKET and LIMIT futures orders directly from the terminal. It is designed with clean architecture in mind — the CLI layer, API layer, validation layer, and logging layer are all fully separated.

The bot is built for **hiring assignment evaluation** and demonstrates real-world backend Python engineering practices including:

- Layered architecture (CLI → validation → business logic → API)
- Typed, documented, PEP8-compliant code
- Structured file logging with rotation
- Robust exception handling for every failure mode
- Professional terminal UX using `rich` and `questionary`

---

## ✅ Features

| Feature | Description |
|---|---|
| MARKET Orders | Instant buy/sell at the current market price |
| LIMIT Orders | Place orders at a specified target price (GTC) |
| BUY / SELL | Both order sides supported |
| Input Validation | All inputs validated before any API call |
| Structured Logging | Timestamped logs in `logs/trading.log` with rotation |
| Rich Terminal UI | Colour-coded tables, panels, and status messages |
| Interactive Mode | Guided prompt-based order entry via `questionary` |
| Confirmation Step | User must confirm before any order is sent |
| Exception Handling | Covers auth failures, API errors, network timeouts |
| Testnet Only | Safe – uses Binance Futures Testnet, no real funds |

---

## 🛠 Tech Stack

| Library | Purpose |
|---|---|
| `python-binance` | Official Binance API wrapper |
| `python-dotenv` | Loads `.env` API credentials |
| `argparse` | CLI argument parsing |
| `rich` | Colour-coded terminal output, tables, panels |
| `questionary` | Interactive prompts for guided order entry |
| `logging` | Structured file + console logging (built-in) |

---

## 📁 Folder Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py          # Package metadata
│   ├── client.py            # Binance client initialisation
│   ├── orders.py            # MARKET / LIMIT order logic
│   ├── validators.py        # Input validation layer
│   ├── logging_config.py    # Logging setup (file + console)
│   └── utils.py             # Terminal output helpers
│
├── logs/
│   └── trading.log          # Rotating structured log file
│
├── .env.example             # Environment variable template
├── .gitignore               # Git exclusions
├── cli.py                   # CLI entry point
├── README.md                # This file
└── requirements.txt         # Pinned dependencies
```

---

## 🌐 Binance Testnet Setup

### Step 1 – Create a Testnet Account

1. Visit **[https://testnet.binancefuture.com](https://testnet.binancefuture.com)**
2. Click **"Log In with GitHub"** (no KYC required – uses your GitHub account)
3. Authorise the connection

### Step 2 – Generate API Keys

1. Once logged in, click your avatar → **"API Management"**
2. Click **"Generate API Key"**
3. Copy both the **API Key** and **API Secret** (the secret is shown only once)

### Step 3 – Check Your Testnet Balance

- Navigate to **"Assets"** in the testnet dashboard
- You should see pre-loaded testnet USDT balance (no deposit required)

### Step 4 – Add Keys to `.env`

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`.

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/binance-futures-testnet-bot.git
cd binance-futures-testnet-bot

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
cp .env.example .env
# Edit .env and add your Testnet API Key and Secret
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `BINANCE_API_KEY` | ✅ Yes | Testnet API Key from Binance Futures Testnet |
| `BINANCE_API_SECRET` | ✅ Yes | Testnet API Secret |

---

## 💻 Usage

### Direct Mode (flags)

```bash
# MARKET BUY
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# MARKET SELL
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.05

# LIMIT BUY
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000

# LIMIT SELL
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 3200.00

# With debug logging
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --log-level DEBUG
```

### Interactive Mode (guided prompts)

```bash
python cli.py --interactive
```

This launches a fully guided order entry flow where you:
- Select symbol, side, order type via prompts
- Enter quantity (and price for LIMIT)
- Review a formatted order summary
- Confirm before the order is sent

### Help

```bash
python cli.py --help
```

---

## 📺 Example Outputs

### MARKET BUY Order

```
╭─────────────────────────────────────────────────╮
│    Binance Futures Testnet Trading Bot           │
│    Testnet environment · Paper trading only      │
╰─────────────────────────────────────────────────╯

──────────────────────────────────────────────────

╭── ORDER REQUEST ─────────────────────────────────╮
│  Symbol        BTCUSDT                           │
│  Side          BUY                               │
│  Order Type    MARKET                            │
│  Quantity      0.001000                          │
│  Timestamp     2024-05-14 09:12:02 UTC           │
╰──────────────────────────────────────────────────╯

──────────────────────────────────────────────────

╭── ORDER RESPONSE ────────────────────────────────╮
│  Order ID      3287641902                        │
│  Symbol        BTCUSDT                           │
│  Side          BUY                               │
│  Type          MARKET                            │
│  Status        FILLED                            │
│  Executed Qty  0.001000                          │
│  Avg Price     103245.12                         │
│  Timestamp     2024-05-14 09:12:03 UTC           │
╰──────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────╮
│  ✅  Order placed successfully.                  │
╰──────────────────────────────────────────────────╯
```

### LIMIT SELL Order

```
╭── ORDER REQUEST ─────────────────────────────────╮
│  Symbol        ETHUSDT                           │
│  Side          SELL                              │
│  Order Type    LIMIT                             │
│  Quantity      0.050000                          │
│  Price         3200.00                           │
│  Timestamp     2024-05-14 10:35:18 UTC           │
╰──────────────────────────────────────────────────╯

╭── ORDER RESPONSE ────────────────────────────────╮
│  Order ID      3287645731                        │
│  Status        NEW                               │
│  Executed Qty  0.000000                          │
│  Avg Price     3200.00                           │
╰──────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────╮
│  ✅  Order placed successfully.                  │
╰──────────────────────────────────────────────────╯
```

### Validation Error

```
╭──────────────────────────────────────────────────╮
│  ❌  Invalid side 'LONG'. Allowed values: BUY, SELL. │
╰──────────────────────────────────────────────────╯
```

---

## 📝 Logging

All activity is logged to `logs/trading.log` using Python's `logging.handlers.RotatingFileHandler`:

- **Max size**: 5 MB per file
- **Backups**: 3 rotated files kept
- **Format**: `timestamp | level | module | message`

### Log Levels

| Level | Usage |
|---|---|
| `DEBUG` | Raw parameter values, validation steps |
| `INFO` | Order requests, responses, connection events |
| `WARNING` | Validation failures, cancelled orders |
| `ERROR` | API errors, network failures, unexpected exceptions |
| `CRITICAL` | Fatal startup errors (bad credentials, unreachable host) |

### Sample Log Entries

```
2024-05-14 09:12:01 | INFO     | trading_bot        | Logging initialised → file: logs/trading.log | level: INFO
2024-05-14 09:12:02 | INFO     | trading_bot.client | Connected to Binance Futures Testnet | server_time=1715680322000
2024-05-14 09:12:02 | INFO     | trading_bot.orders | ORDER REQUEST | symbol=BTCUSDT | side=BUY | type=MARKET | qty=0.001 | price=MARKET
2024-05-14 09:12:03 | INFO     | trading_bot.orders | ORDER RESPONSE | order_id=3287641902 | status=FILLED | executed_qty=0.001 | avg_price=103245.12
2024-05-14 11:47:32 | ERROR    | trading_bot.orders | Binance API error (LIMIT) | code=400 | msg=Margin is insufficient.
```

---

## 🛡 Error Handling

| Error Type | How It's Handled |
|---|---|
| Missing `.env` / API key | `EnvironmentError` caught at startup; clear message shown |
| Invalid symbol / side / type | `ValueError` from validators; displayed before API call |
| Quantity ≤ 0 | Caught in `validate_quantity()`; descriptive error shown |
| LIMIT without price | Caught in `validate_price()`; prompts user to add `--price` |
| `BinanceAPIException` | Caught per-order; error code + message logged and displayed |
| `BinanceRequestException` | Network-level failure; retry guidance shown |
| General `Exception` | Wrapped in `RuntimeError`; logged at ERROR level |
| Keyboard interrupt (Ctrl+C) | Graceful exit in interactive mode via `questionary` |

---

## 🎁 Bonus Feature – Interactive CLI Mode

Run `python cli.py --interactive` for a **fully guided, prompt-based order flow** powered by `questionary` and `rich`:

1. **Symbol prompt** – text input with minimum-length validation
2. **Side selector** – choice between `BUY` and `SELL`
3. **Order type selector** – choice between `MARKET` and `LIMIT`
4. **Quantity prompt** – validated as a positive float
5. **Price prompt** – shown only for LIMIT orders
6. **Formatted preview** – complete order summary table printed before submission
7. **Confirmation step** – user types `y/n` to confirm or cancel

All interactive inputs are re-validated using the same validators as direct mode.

---

## 📌 Assumptions

1. **Testnet only** – the `testnet=True` flag is hardcoded; this bot is not intended for mainnet trading.
2. **USDT-M Futures** – only USDT-margined perpetual contracts are targeted.
3. **GTC time-in-force** – all LIMIT orders use Good Till Cancel by default.
4. **Quantity precision** – the user is responsible for using a quantity that satisfies Binance's `LOT_SIZE` filter for the chosen symbol.
5. **Symbol validity** – the bot validates format (uppercase letters) but does not pre-check whether the pair is listed on the testnet.
6. **Single-order CLI** – each invocation places exactly one order; loop/batch trading is out of scope.

---

## 🐙 GitHub Strategy

### Recommended Repository Name

```
binance-futures-testnet-bot
```

### Professional Description

```
A clean, modular Python CLI bot for placing MARKET & LIMIT orders on the Binance Futures Testnet.
Built with python-binance, rich terminal UI, structured logging, and full input validation.
```

### Recommended Topics / Tags

```
python binance binance-api futures trading-bot cli testnet python-binance
argparse rich algorithmic-trading cryptocurrency
```

### Commit Message Strategy

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add interactive CLI mode with questionary prompts
feat: implement LIMIT order support with GTC time-in-force
fix: handle BinanceAPIException on insufficient margin
chore: add rotating file handler to logging config
docs: complete README with testnet setup guide
refactor: separate order dispatch from order placement logic
test: add unit tests for validators module
```

---

## 📄 License

MIT © 2024
