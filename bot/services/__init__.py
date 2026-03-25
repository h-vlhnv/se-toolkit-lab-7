"""Services for external API clients.

This module provides clients for interacting with:
- LMS Backend API
- LLM API for intent recognition
"""

from .lms_client import LMSClient
from .llm_client import LLMClient

__all__ = ["LMSClient", "LLMClient"]
