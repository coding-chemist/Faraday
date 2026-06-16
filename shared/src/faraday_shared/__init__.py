"""Faraday cross-cutting concerns: config, logging, common types."""
from faraday_shared.config import settings
from faraday_shared.logging import get_logger, setup_logging

__all__ = ["settings", "get_logger", "setup_logging"]
