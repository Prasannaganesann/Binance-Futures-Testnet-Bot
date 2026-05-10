"""
Utilities
==========
Shared helper functions used across the trading bot.

Responsibilities:
    - Terminal output formatting (request summary, response table)
    - Rich console helpers (colour, panels, separators)
    - Timestamp generation
    - Safe float formatting
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from bot.logging_config import get_logger

logger = get_logger("utils")
console = Console()


# ── Timestamp ────────────────────────────────────────────────────────────────

def utc_now() -> str:
    """Return current UTC timestamp as an ISO-8601 string."""
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


# ── Formatting helpers ────────────────────────────────────────────────────────

def _fmt_float(value: Any, decimals: int = 8) -> str:
    """Safely format a value as a fixed-decimal float string."""
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


# ── Terminal output ──────────────────────────────────────────────────────────

def print_order_request(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> None:
    """
    Print a formatted order-request summary to the terminal.

    Args:
        symbol:     Trading pair.
        side:       BUY / SELL.
        order_type: MARKET / LIMIT.
        quantity:   Order quantity.
        price:      Limit price (None for MARKET).
    """
    table = Table(
        title="ORDER REQUEST",
        box=box.ROUNDED,
        title_style="bold cyan",
        show_header=False,
        padding=(0, 2),
        style="dim",
    )
    table.add_column("Field", style="bold white", min_width=14)
    table.add_column("Value", style="bright_white")

    side_colour = "green" if side == "BUY" else "red"

    table.add_row("Symbol", f"[yellow]{symbol}[/yellow]")
    table.add_row("Side", f"[{side_colour}]{side}[/{side_colour}]")
    table.add_row("Order Type", order_type)
    table.add_row("Quantity", _fmt_float(quantity, 6))

    if order_type == "LIMIT" and price is not None:
        table.add_row("Price", f"[cyan]{_fmt_float(price, 2)}[/cyan]")

    table.add_row("Timestamp", utc_now())

    console.print()
    console.print(table)
    console.print()


def print_order_response(result: dict) -> None:
    """
    Print a formatted order-response summary to the terminal.

    Args:
        result: Normalised OrderResult dict from orders.py.
    """
    status = result.get("status", "UNKNOWN")
    status_colour = "green" if status in ("FILLED", "NEW") else "yellow"

    table = Table(
        title="ORDER RESPONSE",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=False,
        padding=(0, 2),
        style="dim",
    )
    table.add_column("Field", style="bold white", min_width=14)
    table.add_column("Value", style="bright_white")

    table.add_row("Order ID", str(result.get("order_id", "N/A")))
    table.add_row("Symbol", str(result.get("symbol", "N/A")))
    table.add_row("Side", str(result.get("side", "N/A")))
    table.add_row("Type", str(result.get("type", "N/A")))
    table.add_row("Status", f"[{status_colour}]{status}[/{status_colour}]")
    table.add_row("Executed Qty", _fmt_float(result.get("executed_qty", 0), 6))
    table.add_row("Avg Price", _fmt_float(result.get("avg_price", 0), 2))
    table.add_row("Timestamp", utc_now())

    console.print(table)
    console.print()


def print_success(message: str = "Order placed successfully.") -> None:
    """Print a styled success banner."""
    console.print(
        Panel(
            f":white_check_mark:  [bold green]{message}[/bold green]",
            border_style="green",
            expand=False,
        )
    )
    console.print()


def print_error(message: str) -> None:
    """Print a styled error banner."""
    console.print(
        Panel(
            f":x:  [bold red]{message}[/bold red]",
            border_style="red",
            expand=False,
        )
    )
    console.print()


def print_warning(message: str) -> None:
    """Print a styled warning banner."""
    console.print(
        Panel(
            f":warning:  [bold yellow]{message}[/bold yellow]",
            border_style="yellow",
            expand=False,
        )
    )
    console.print()


def print_separator() -> None:
    """Print a visual separator line."""
    console.rule(style="dim")


def print_banner() -> None:
    """Print the application start banner."""
    banner = (
        "[bold cyan]Binance Futures Testnet Trading Bot[/bold cyan]\n"
        "[dim]Testnet environment · Paper trading only[/dim]"
    )
    console.print(
        Panel(banner, border_style="cyan", padding=(1, 4), expand=False)
    )
    console.print()
