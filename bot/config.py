"""Configuration management for the LMS Telegram Bot.

Loads environment variables from .env.bot.secret using pydantic-settings.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Bot configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env.bot.secret",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Telegram Bot
    bot_token: str | None = None

    # LMS Backend API
    lms_api_base_url: str = "http://localhost:8000"
    lms_api_key: str | None = None

    # LLM API
    llm_api_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"
    llm_api_model: str = "coder-model"

    @property
    def is_test_mode(self) -> bool:
        """Check if running in test mode (no Telegram connection)."""
        return self.bot_token is None

    @property
    def has_lms_api(self) -> bool:
        """Check if LMS API is configured."""
        return bool(self.lms_api_base_url and self.lms_api_key)

    @property
    def has_llm_api(self) -> bool:
        """Check if LLM API is configured."""
        return bool(self.llm_api_base_url and self.llm_api_key)


def load_settings() -> BotSettings:
    """Load bot settings from environment.
    
    Returns:
        BotSettings instance with loaded configuration.
    """
    return BotSettings()
