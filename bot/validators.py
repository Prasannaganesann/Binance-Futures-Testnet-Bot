"""
Input Validators
=================
All CLI / programmatic input validation logic lives here.
Keeps the CLI layer and API layer completely decoupled from
raw string sanitisation concerns.

Raises:
    ValueError  – on any invalid input with a human-readable message.
"""

from __future__ import annotations

import re
from typing import Optional

from bot.logging_config import get_logger

logger = get_logger("validators")

# ── Constants ────────────────────────────────────────────────────────────────

VALID_SIDES: set[str] = {"BUY", "SELL"}
VALID_ORDER_TYPES: set[str] = {"MARKET", "LIMIT"}

# Binance symbol format: 2-10 uppercase letters (e.g. BTCUSDT, ETHUSDT)
SYMBOL_PATTERN = re.compile(r"^[A-Z]{2,12}$")


# ── Public validators ────────────────────────────────────────────────────────

def validate_symbol(symbol: str) -> str:
    """
    Validate and normalise a trading pair symbol.

    Args:
        symbol: Raw symbol string (e.g. 'btcusdt', 'BTCUSDT').

    Returns:
        Upper-cased, stripped symbol string.

    Raises:
        ValueError: If the symbol does not match the expected format.
    """
    normalised = symbol.strip().upper()
    if not SYMBOL_PATTERN.match(normalised):
        msg = (
            f"Invalid symbol '{symbol}'. "
            "Expected 2–12 uppercase letters (e.g. BTCUSDT, ETHUSDT)."
        )
        logger.warning("Symbol validation failed: %s", msg)
        raise ValueError(msg)

    logger.debug("Symbol validated: %s", normalised)
    return normalised


def validate_side(side: str) -> str:
    """
    Validate order side.

    Args:
        side: 'BUY' or 'SELL' (case-insensitive).

    Returns:
        Upper-cased side string.

    Raises:
        ValueError: If side is not BUY or SELL.
    """
    normalised = side.strip().upper()
    if normalised not in VALID_SIDES:
        msg = (
            f"Invalid side '{side}'. "
            f"Allowed values: {', '.join(sorted(VALID_SIDES))}."
        )
        logger.warning("Side validation failed: %s", msg)
        raise ValueError(msg)

    logger.debug("Side validated: %s", normalised)
    return normalised


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.

    Args:
        order_type: 'MARKET' or 'LIMIT' (case-insensitive).

    Returns:
        Upper-cased order type string.

    Raises:
        ValueError: If order type is not supported.
    """
    normalised = order_type.strip().upper()
    if normalised not in VALID_ORDER_TYPES:
        msg = (
            f"Invalid order type '{order_type}'. "
            f"Allowed values: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )
        logger.warning("Order type validation failed: %s", msg)
        raise ValueError(msg)

    logger.debug("Order type validated: %s", normalised)
    return normalised


def validate_quantity(quantity: str | float) -> float:
    """
    Validate order quantity.

    Args:
        quantity: Raw quantity value (string or numeric).

    Returns:
        Validated float quantity.

    Raises:
        ValueError: If quantity is non-numeric or not > 0.
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        msg = f"Invalid quantity '{quantity}'. Must be a positive numeric value."
        logger.warning("Quantity validation failed: %s", msg)
        raise ValueError(msg)

    if qty <= 0:
        msg = f"Quantity must be greater than 0. Got: {qty}."
        logger.warning("Quantity validation failed: %s", msg)
        raise ValueError(msg)

    logger.debug("Quantity validated: %s", qty)
    return qty


def validate_price(price: Optional[str | float], order_type: str) -> Optional[float]:
    """
    Validate order price.

    For LIMIT orders, a positive numeric price is mandatory.
    For MARKET orders, price must be None (ignored if provided).

    Args:
        price:      Raw price value or None.
        order_type: 'MARKET' or 'LIMIT' (already validated).

    Returns:
        Validated float price for LIMIT orders, None for MARKET.

    Raises:
        ValueError: If LIMIT order lacks price, or price is invalid.
    """
    if order_type == "MARKET":
        if price is not None:
            logger.debug("Price ignored for MARKET order.")
        return None

    # LIMIT order path
    if price is None:
        msg = "Price is required for LIMIT orders."
        logger.warning("Price validation failed: %s", msg)
        raise ValueError(msg)

    try:
        p = float(price)
    except (ValueError, TypeError):
        msg = f"Invalid price '{price}'. Must be a positive numeric value."
        logger.warning("Price validation failed: %s", msg)
        raise ValueError(msg)

    if p <= 0:
        msg = f"Price must be greater than 0. Got: {p}."
        logger.warning("Price validation failed: %s", msg)
        raise ValueError(msg)

    logger.debug("Price validated: %s", p)
    return p


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str | float,
    price: Optional[str | float] = None,
) -> dict:
    """
    Run all validators and return a clean, typed parameter dict.

    Args:
        symbol:     Trading pair (e.g. 'BTCUSDT').
        side:       'BUY' or 'SELL'.
        order_type: 'MARKET' or 'LIMIT'.
        quantity:   Order quantity.
        price:      Order price (required for LIMIT, ignored for MARKET).

    Returns:
        Dict with keys: symbol, side, order_type, quantity, price.

    Raises:
        ValueError: On any validation failure.
    """
    logger.info("Running full input validation …")

    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_type = validate_order_type(order_type)
    validated_qty = validate_quantity(quantity)
    validated_price = validate_price(price, validated_type)

    logger.info("All inputs validated successfully.")

    return {
        "symbol": validated_symbol,
        "side": validated_side,
        "order_type": validated_type,
        "quantity": validated_qty,
        "price": validated_price,
    }
