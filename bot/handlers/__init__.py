"""Command handlers for the LMS Telegram Bot.

Handlers are pure functions that take input and return text responses.
They have no dependency on Telegram, making them testable in isolation.
"""

from .base import (
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
    handle_start,
    handle_text,
)

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
    "handle_text",
]
