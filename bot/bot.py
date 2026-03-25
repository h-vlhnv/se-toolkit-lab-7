#!/usr/bin/env python3
"""LMS Telegram Bot entry point.

Supports two modes:
1. Test mode: `uv run bot.py --test "/command"` - prints response to stdout
2. Telegram mode: Connects to Telegram and handles messages in real-time
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from typing import NoReturn

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import load_settings
from handlers import (
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
    handle_start,
    handle_text,
)
from services import LMSClient, LLMClient


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="LMS Telegram Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--test",
        type=str,
        metavar="INPUT",
        help="Run in test mode with the given input (e.g., '/start' or 'hello')",
    )
    return parser.parse_args()


async def run_test_mode(input_text: str) -> NoReturn:
    """Run bot in test mode - call handlers directly without Telegram.
    
    Args:
        input_text: The input to test (e.g., "/start", "/help", "what labs are available")
    """
    input_text = input_text.strip()
    
    # Route to appropriate handler based on input
    if input_text == "/start":
        response = handle_start()
    elif input_text == "/help":
        response = handle_help()
    elif input_text == "/health":
        response = handle_health()
    elif input_text == "/labs":
        response = handle_labs()
    elif input_text.startswith("/scores"):
        # Extract lab name if provided
        parts = input_text.split(maxsplit=1)
        lab_name = parts[1] if len(parts) > 1 else None
        response = handle_scores(lab_name)
    else:
        # Plain text message - use text handler
        response = handle_text(input_text)
    
    print(response)
    sys.exit(0)


async def run_telegram_mode() -> None:
    """Run bot in Telegram mode - connect to Telegram and handle messages."""
    settings = load_settings()
    
    if not settings.bot_token:
        print("Error: BOT_TOKEN not set. Cannot run in Telegram mode.")
        print("Set BOT_TOKEN in .env.bot.secret or use --test mode for offline testing.")
        sys.exit(1)
    
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    
    # Initialize service clients
    lms_client = LMSClient(
        base_url=settings.lms_api_base_url,
        api_key=settings.lms_api_key,
    )
    llm_client = LLMClient(
        api_key=settings.llm_api_key,
        base_url=settings.llm_api_base_url,
        model=settings.llm_api_model,
    )
    
    # Store clients in dispatcher storage for handlers to access
    dp["lms_client"] = lms_client
    dp["llm_client"] = llm_client
    
    # Register command handlers
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_health, Command("health"))
    dp.message.register(cmd_labs, Command("labs"))
    dp.message.register(cmd_scores, Command("scores"))
    dp.message.register(handle_plain_text)
    
    # Start polling
    print("Bot is starting in Telegram mode...")
    await dp.start_polling(bot)


async def cmd_start(message: Message) -> None:
    """Handle /start command."""
    response = handle_start()
    await message.answer(response)


async def cmd_help(message: Message) -> None:
    """Handle /help command."""
    response = handle_help()
    await message.answer(response)


async def cmd_health(message: Message) -> None:
    """Handle /health command."""
    # Will be enhanced in Task 2 to call real backend
    response = handle_health()
    await message.answer(response)


async def cmd_labs(message: Message) -> None:
    """Handle /labs command."""
    # Will be enhanced in Task 2 to call real backend
    response = handle_labs()
    await message.answer(response)


async def cmd_scores(message: Message) -> None:
    """Handle /scores command with optional lab name argument."""
    # Extract lab name from command arguments
    lab_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    response = handle_scores(lab_name)
    await message.answer(response)


async def handle_plain_text(message: Message) -> None:
    """Handle plain text messages using LLM for intent routing."""
    if not message.text:
        return
    response = handle_text(message.text)
    await message.answer(response)


async def main() -> None:
    """Main entry point."""
    args = parse_args()
    
    if args.test:
        await run_test_mode(args.test)
    else:
        await run_telegram_mode()


if __name__ == "__main__":
    asyncio.run(main())
