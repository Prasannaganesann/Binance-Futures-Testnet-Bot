"""
Logging Configuration
======================
Configures structured logging for the trading bot.

Features:
    - Console handler with INFO level
    - File handler writing to logs/trading.log
    - Timestamped, leveled log entries
    - Rotating log support (optional)
"""

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "trading.log")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Initialize and configure the application-wide logger.

    Sets up two handlers:
        1. StreamHandler  – prints INFO+ to stdout
        2. RotatingFileHandler – writes all levels to logs/trading.log
                                 (max 5 MB per file, up to 3 backups)

    Args:
        log_level: Logging level string (DEBUG, INFO, WARNING, ERROR).

    Returns:
        Configured root logger for the 'trading_bot' namespace.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)  # Capture everything; handlers filter

    if logger.handlers:
        # Prevent duplicate handlers on repeated calls
        logger.handlers.clear()

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # ── Console handler ──────────────────────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)

    # ── File handler (rotating) ──────────────────────────────────────────────
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Logging initialised → file: %s | level: %s", LOG_FILE, log_level)
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Retrieve a child logger under the 'trading_bot' namespace.

    Args:
        name: Sub-module name (e.g. 'orders', 'client').

    Returns:
        Child Logger instance.
    """
    return logging.getLogger(f"trading_bot.{name}")
