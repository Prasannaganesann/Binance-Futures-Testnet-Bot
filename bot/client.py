"""
Binance Futures Testnet Client
================================
Handles authenticated connection to the Binance Futures Testnet.

Environment variables required (loaded via python-dotenv):
    BINANCE_API_KEY     – Testnet API key
    BINANCE_API_SECRET  – Testnet API secret

The module intentionally keeps client construction separate from
business logic so it can be swapped (e.g. mainnet vs testnet) via
config without touching order or validator code.
"""

from __future__ import annotations

import os
from typing import Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

from bot.logging_config import get_logger

logger = get_logger("client")

# ── Testnet base URLs ────────────────────────────────────────────────────────
FUTURES_TESTNET_BASE_URL = "https://testnet.binancefuture.com"


def load_credentials() -> tuple[str, str]:
    """
    Load API credentials from environment variables.

    Looks for:
        BINANCE_API_KEY
        BINANCE_API_SECRET

    Returns:
        (api_key, api_secret) tuple of strings.

    Raises:
        EnvironmentError: If either credential is missing.
    """
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key:
        raise EnvironmentError(
            "BINANCE_API_KEY not found. "
            "Set it in your .env file or as an environment variable."
        )
    if not api_secret:
        raise EnvironmentError(
            "BINANCE_API_SECRET not found. "
            "Set it in your .env file or as an environment variable."
        )

    logger.debug("API credentials loaded from environment.")
    return api_key, api_secret


def get_client(testnet: bool = True) -> Client:
    """
    Build and return an authenticated Binance Client instance.

    Args:
        testnet: When True (default), connects to Binance Futures Testnet.
                 Set to False only for mainnet use (outside this assignment).

    Returns:
        Authenticated binance.client.Client instance.

    Raises:
        EnvironmentError:        Missing API credentials.
        BinanceAPIException:     API-level authentication error.
        BinanceRequestException: Network / request failure during handshake.
        ConnectionError:         General connectivity failure.
    """
    api_key, api_secret = load_credentials()

    logger.info(
        "Initialising Binance client | testnet=%s | base_url=%s",
        testnet,
        FUTURES_TESTNET_BASE_URL if testnet else "mainnet",
    )

    try:
        client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet,
        )

        # Override the futures testnet endpoint explicitly
        if testnet:
            client.FUTURES_URL = FUTURES_TESTNET_BASE_URL + "/fapi"

        # Quick connectivity check – fetch server time
        server_time = client.get_server_time()
        logger.info(
            "Connected to Binance Futures Testnet | server_time=%s",
            server_time.get("serverTime"),
        )

        return client

    except BinanceAPIException as exc:
        logger.error(
            "Authentication failed | code=%s | msg=%s", exc.status_code, exc.message
        )
        raise

    except BinanceRequestException as exc:
        logger.error("Network error during client initialisation: %s", exc)
        raise

    except Exception as exc:
        logger.error("Unexpected error initialising Binance client: %s", exc)
        raise ConnectionError(
            f"Could not connect to Binance Futures Testnet: {exc}"
        ) from exc
