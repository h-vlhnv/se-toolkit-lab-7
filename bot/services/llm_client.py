"""LLM API client for intent recognition.

Provides methods to interact with the LLM for natural language understanding.
"""

from __future__ import annotations

import httpx


class LLMClient:
    """Client for the LLM API."""

    def __init__(self, api_key: str, base_url: str, model: str = "coder-model") -> None:
        """Initialize the LLM client.
        
        Args:
            api_key: API key for the LLM service.
            base_url: Base URL of the LLM API.
            model: Model name to use for inference.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0,
        )

    async def parse_intent(self, user_message: str) -> dict:
        """Parse user message to detect intent and extract parameters.
        
        Args:
            user_message: The user's text message.
            
        Returns:
            Dictionary with detected intent and extracted parameters.
        """
        # Placeholder implementation - will be connected to real LLM in Task 3
        return {
            "intent": "unknown",
            "parameters": {},
            "confidence": 0.0,
        }

    async def chat(self, messages: list[dict]) -> str:
        """Send a chat request to the LLM.
        
        Args:
            messages: List of message dictionaries with role and content.
            
        Returns:
            LLM response text.
        """
        try:
            response = await self._client.post(
                "/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except httpx.HTTPError:
            return "Sorry, I'm having trouble connecting to the AI service right now."

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
