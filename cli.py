#!/usr/bin/env python3
"""
cli.py – Binance Futures Testnet Trading Bot
=============================================
Entry point for the trading bot CLI.

Modes:
    1. Direct mode   – pass all arguments via flags (--symbol, --side, …)
    2. Interactive   – run with `--interactive` for a guided prompt-based flow

Usage (direct mode):
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

Usage (interactive mode):
    python cli.py --interactive

Usage (with logging level override):
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT \\
                  --quantity 0.01 --price 60000 --log-level DEBUG
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

import questionary
from rich.console import Console

from bot.client import get_client
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.utils import (
    print_banner,
    print_error,
    print_order_request,
    print_order_response,
    print_separator,
    print_success,
    print_warning,
)
from bot.validators import validate_all

console = Console()


# ── Argument parser ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description=(
            "Binance Futures Testnet Trading Bot – "
            "Place MARKET and LIMIT futures orders from the command line."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # MARKET BUY
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # LIMIT SELL
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 3200.00

  # Interactive mode
  python cli.py --interactive
        """,
    )

    parser.add_argument(
        "--symbol", "-s",
        type=str,
        help="Trading pair symbol (e.g. BTCUSDT, ETHUSDT).",
    )
    parser.add_argument(
        "--side",
        type=str,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL.",
    )
    parser.add_argument(
        "--type", "-t",
        dest="order_type",
        type=str,
        choices=["MARKET", "LIMIT", "market", "limit"],
        help="Order type: MARKET or LIMIT.",
    )
    parser.add_argument(
        "--quantity", "-q",
        type=str,
        help="Order quantity (must be > 0).",
    )
    parser.add_argument(
        "--price", "-p",
        type=str,
        default=None,
        help="Limit price per unit (required for LIMIT orders).",
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        default=False,
        help="Launch interactive guided order menu.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO).",
    )

    return parser


# ── Interactive mode ─────────────────────────────────────────────────────────

def interactive_flow() -> Optional[dict]:
    """
    Guided, prompt-based order configuration using questionary.

    Returns:
        Validated parameter dict, or None if the user cancels.
    """
    console.print("[bold cyan]Interactive Order Configurator[/bold cyan]\n")

    # ── Symbol ───────────────────────────────────────────────────────────────
    symbol = questionary.text(
        "Enter trading pair symbol:",
        default="BTCUSDT",
        validate=lambda v: (
            True if len(v.strip()) >= 4
            else "Symbol must be at least 4 characters (e.g. BTCUSDT)"
        ),
    ).ask()

    if symbol is None:
        return None  # User pressed Ctrl+C

    # ── Side ─────────────────────────────────────────────────────────────────
    side = questionary.select(
        "Select order side:",
        choices=["BUY", "SELL"],
    ).ask()

    if side is None:
        return None

    # ── Order type ───────────────────────────────────────────────────────────
    order_type = questionary.select(
        "Select order type:",
        choices=["MARKET", "LIMIT"],
    ).ask()

    if order_type is None:
        return None

    # ── Quantity ─────────────────────────────────────────────────────────────
    quantity_raw = questionary.text(
        "Enter quantity:",
        validate=lambda v: (
            True
            if _is_positive_float(v)
            else "Quantity must be a positive number (e.g. 0.001)"
        ),
    ).ask()

    if quantity_raw is None:
        return None

    # ── Price (LIMIT only) ───────────────────────────────────────────────────
    price_raw: Optional[str] = None
    if order_type == "LIMIT":
        price_raw = questionary.text(
            "Enter limit price:",
            validate=lambda v: (
                True
                if _is_positive_float(v)
                else "Price must be a positive number (e.g. 65000.00)"
            ),
        ).ask()

        if price_raw is None:
            return None

    # ── Validate ─────────────────────────────────────────────────────────────
    try:
        params = validate_all(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity_raw,
            price=price_raw,
        )
    except ValueError as exc:
        print_error(str(exc))
        return None

    # ── Confirmation ─────────────────────────────────────────────────────────
    console.print()
    print_order_request(
        symbol=params["symbol"],
        side=params["side"],
        order_type=params["order_type"],
        quantity=params["quantity"],
        price=params["price"],
    )

    confirmed = questionary.confirm(
        "Confirm and place this order?",
        default=False,
    ).ask()

    if not confirmed:
        print_warning("Order cancelled by user.")
        return None

    return params


# ── Direct mode ──────────────────────────────────────────────────────────────

def direct_flow(args: argparse.Namespace) -> Optional[dict]:
    """
    Validate and return order params from CLI flags.

    Args:
        args: Parsed argparse.Namespace.

    Returns:
        Validated parameter dict, or None on validation error.
    """
    missing = [
        flag
        for flag, val in [
            ("--symbol", args.symbol),
            ("--side", args.side),
            ("--type", args.order_type),
            ("--quantity", args.quantity),
        ]
        if not val
    ]

    if missing:
        print_error(
            f"Missing required arguments for direct mode: {', '.join(missing)}.\n"
            "Use --interactive for guided input, or pass all required flags."
        )
        return None

    try:
        params = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as exc:
        print_error(str(exc))
        return None

    return params


# ── Helpers ──────────────────────────────────────────────────────────────────

def _is_positive_float(value: str) -> bool:
    """Return True if value is a parseable positive float."""
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False


# ── Main execution ───────────────────────────────────────────────────────────

def main() -> None:
    """Main entry point: parse args, validate, connect, place order."""
    parser = build_parser()
    args = parser.parse_args()

    # ── Logging setup ─────────────────────────────────────────────────────
    logger = setup_logging(args.log_level)

    # ── Banner ────────────────────────────────────────────────────────────
    print_banner()
    print_separator()

    # ── Gather order parameters ───────────────────────────────────────────
    if args.interactive:
        params = interactive_flow()
    else:
        params = direct_flow(args)

    if params is None:
        logger.warning("Order flow exited without placing an order.")
        sys.exit(0)

    # ── Print request summary (direct mode only; interactive shows it above) ─
    if not args.interactive:
        print_order_request(
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
        )

    print_separator()

    # ── Connect to Binance Testnet ────────────────────────────────────────
    console.print("[dim]Connecting to Binance Futures Testnet …[/dim]")

    try:
        client = get_client(testnet=True)
    except EnvironmentError as exc:
        print_error(f"Configuration error: {exc}")
        logger.critical("Environment error: %s", exc)
        sys.exit(1)
    except Exception as exc:
        print_error(f"Connection failed: {exc}")
        logger.critical("Connection error: %s", exc)
        sys.exit(1)

    console.print("[dim]Connected.[/dim]\n")

    # ── Place order ───────────────────────────────────────────────────────
    try:
        result = place_order(
            client=client,
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
        )
    except Exception as exc:
        print_error(f"Order failed: {exc}")
        logger.error("Order placement error: %s", exc)
        sys.exit(1)

    # ── Display result ────────────────────────────────────────────────────
    print_separator()
    print_order_response(result)
    print_success("Order placed successfully.")
    logger.info("Order completed | order_id=%s", result.get("order_id"))


if __name__ == "__main__":
    main()
