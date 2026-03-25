"""LMS Backend API client.

Provides methods to interact with the Learning Management System backend.
"""

from __future__ import annotations

import httpx


class LMSClient:
    """Client for the LMS Backend API."""

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        """Initialize the LMS client.
        
        Args:
            base_url: Base URL of the LMS backend API.
            api_key: Optional API key for authentication.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
            timeout=30.0,
        )

    async def health_check(self) -> bool:
        """Check if the backend is healthy.
        
        Returns:
            True if backend is up and responding, False otherwise.
        """
        try:
            response = await self._client.get("/health")
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    async def get_labs(self) -> list[dict]:
        """Get list of available labs.
        
        Returns:
            List of lab dictionaries with lab information.
        """
        try:
            response = await self._client.get("/labs")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return []

    async def get_scores(self, lab_name: str) -> dict | None:
        """Get scores for a specific lab.
        
        Args:
            lab_name: Name of the lab to get scores for.
            
        Returns:
            Dictionary with scores information or None if not found.
        """
        try:
            response = await self._client.get(f"/scores/{lab_name}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
