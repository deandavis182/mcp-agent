"""Application-wide logging utilities."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from typing import Any


LOG_FILE = "mcp-agent.log"


def _configure_logger() -> logging.Logger:
    """Configure and return the shared application logger."""

    logger = logging.getLogger("mcp-agent")
    if logger.handlers:
        # Already configured
        return logger

    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = _configure_logger()


def _mask_api_key(key: str | None) -> str:
    """Return a masked representation of an API key."""

    if not key:
        return ""
    if len(key) <= 4:
        return "*" * len(key)
    return key[:2] + "*" * (len(key) - 4) + key[-2:]


def log_invocation(endpoint: str, args: dict[str, Any] | None, api_key: str | None) -> None:
    """Log a request invocation.

    Parameters
    ----------
    endpoint:
        The requested endpoint path.
    args:
        Dictionary of arguments supplied by the caller.
    api_key:
        The raw API key provided with the request.
    """

    logger.info(
        "endpoint=%s args=%s api_key=%s",
        endpoint,
        args or {},
        _mask_api_key(api_key),
    )


__all__ = ["logger", "log_invocation"]

