"""
Order Placement
================
Encapsulates all Binance Futures order-placement logic.

Supported order types:
    - MARKET  (BUY / SELL)
    - LIMIT   (BUY / SELL) with GTC time-in-force

All public functions return a normalised OrderResult dict so
the CLI / UI layer never has to inspect raw Binance responses.
"""

from __future__ import annotations

from typing import Any, Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.logging_config import get_logger

logger = get_logger("orders")

# ── Types ────────────────────────────────────────────────────────────────────

OrderResult = dict[str, Any]


# ── Internal helpers ─────────────────────────────────────────────────────────

def _parse_response(raw: dict) -> OrderResult:
    """
    Normalise a raw Binance Futures order response into a clean dict.

    Args:
        raw: The dict returned directly by the python-binance library.

    Returns:
        OrderResult with standardised keys:
            order_id, symbol, side, type, status,
            executed_qty, avg_price, raw
    """
    avg_price = raw.get("avgPrice") or raw.get("price") or "N/A"

    result: OrderResult = {
        "order_id": raw.get("orderId"),
        "symbol": raw.get("symbol"),
        "side": raw.get("side"),
        "type": raw.get("type"),
        "status": raw.get("status"),
        "executed_qty": raw.get("executedQty", "0"),
        "avg_price": avg_price,
        "raw": raw,
    }

    logger.debug("Parsed order response: %s", result)
    return result


def _log_request(symbol: str, side: str, order_type: str, quantity: float,
                 price: Optional[float]) -> None:
    """Log outgoing order request details."""
    logger.info(
        "ORDER REQUEST | symbol=%s | side=%s | type=%s | qty=%s | price=%s",
        symbol,
        side,
        order_type,
        quantity,
        price if price is not None else "MARKET",
    )


def _log_response(result: OrderResult) -> None:
    """Log incoming order response details."""
    logger.info(
        "ORDER RESPONSE | order_id=%s | status=%s | executed_qty=%s | avg_price=%s",
        result["order_id"],
        result["status"],
        result["executed_qty"],
        result["avg_price"],
    )


# ── Public API ───────────────────────────────────────────────────────────────

def place_market_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
) -> OrderResult:
    """
    Place a MARKET order on Binance Futures Testnet.

    Args:
        client:   Authenticated Binance Client instance.
        symbol:   Trading pair (e.g. 'BTCUSDT').
        side:     'BUY' or 'SELL'.
        quantity: Number of units to trade.

    Returns:
        Normalised OrderResult dict.

    Raises:
        BinanceAPIException:     Binance rejected the order.
        BinanceRequestException: Network-level failure.
        RuntimeError:            Unexpected errors.
    """
    _log_request(symbol, side, "MARKET", quantity, None)

    try:
        raw = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
    except BinanceAPIException as exc:
        logger.error(
            "Binance API error (MARKET) | code=%s | msg=%s",
            exc.status_code,
            exc.message,
        )
        raise
    except BinanceRequestException as exc:
        logger.error("Network error placing MARKET order: %s", exc)
        raise
    except Exception as exc:
        logger.error("Unexpected error placing MARKET order: %s", exc)
        raise RuntimeError(f"Unexpected error: {exc}") from exc

    result = _parse_response(raw)
    _log_response(result)
    return result


def place_limit_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> OrderResult:
    """
    Place a LIMIT order on Binance Futures Testnet.

    Args:
        client:        Authenticated Binance Client instance.
        symbol:        Trading pair (e.g. 'BTCUSDT').
        side:          'BUY' or 'SELL'.
        quantity:      Number of units to trade.
        price:         Limit price per unit.
        time_in_force: Order duration policy. Default: GTC (Good Till Cancel).

    Returns:
        Normalised OrderResult dict.

    Raises:
        BinanceAPIException:     Binance rejected the order.
        BinanceRequestException: Network-level failure.
        RuntimeError:            Unexpected errors.
    """
    _log_request(symbol, side, "LIMIT", quantity, price)

    try:
        raw = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce=time_in_force,
        )
    except BinanceAPIException as exc:
        logger.error(
            "Binance API error (LIMIT) | code=%s | msg=%s",
            exc.status_code,
            exc.message,
        )
        raise
    except BinanceRequestException as exc:
        logger.error("Network error placing LIMIT order: %s", exc)
        raise
    except Exception as exc:
        logger.error("Unexpected error placing LIMIT order: %s", exc)
        raise RuntimeError(f"Unexpected error: {exc}") from exc

    result = _parse_response(raw)
    _log_response(result)
    return result


def place_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> OrderResult:
    """
    Unified order dispatcher – routes to MARKET or LIMIT handler.

    Args:
        client:     Authenticated Binance Client instance.
        symbol:     Trading pair (e.g. 'BTCUSDT').
        side:       'BUY' or 'SELL'.
        order_type: 'MARKET' or 'LIMIT'.
        quantity:   Number of units.
        price:      Required for LIMIT; ignored for MARKET.

    Returns:
        Normalised OrderResult dict.

    Raises:
        ValueError:              Unknown order type.
        BinanceAPIException:     Binance API error.
        BinanceRequestException: Network error.
    """
    logger.info(
        "Dispatching order | type=%s | symbol=%s | side=%s | qty=%s",
        order_type, symbol, side, quantity,
    )

    if order_type == "MARKET":
        return place_market_order(client, symbol, side, quantity)

    elif order_type == "LIMIT":
        if price is None:
            raise ValueError("Price must not be None for LIMIT orders.")
        return place_limit_order(client, symbol, side, quantity, price)

    else:
        raise ValueError(f"Unsupported order type: '{order_type}'")
