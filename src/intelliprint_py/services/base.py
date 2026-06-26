"""Base service class for Intelliprint API."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import requests

from intelliprint_py.exceptions import IntelliprintError

if TYPE_CHECKING:
    from intelliprint_py.client import IntelliprintClient

logger = logging.getLogger(__name__)


class BaseService:
    """Base service class providing common HTTP request functionality.

    All service classes inherit from this base class to share
    authentication and request handling logic.

    Attributes:
        client: The parent IntelliprintClient instance.
    """

    BASE_URL = "https://api.intelliprint.net/v1"
    TIMEOUT = 30

    def __init__(self, client: IntelliprintClient) -> None:
        """Initialize the base service.

        Args:
            client: The parent IntelliprintClient instance.
        """
        self._client = client

    @property
    def _headers(self) -> dict[str, str]:
        """Get the request headers for API calls.

        Returns:
            Dictionary containing the Authorization and Content-Type headers.
        """
        return {
            "Authorization": self._client.api_key,
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the Intelliprint API.

        Args:
            method: HTTP method (GET, POST, DELETE).
            endpoint: API endpoint path (e.g., '/prints').
            json_data: JSON data to send in the request body.
            files: Files to upload (for multipart/form-data requests).

        Returns:
            The JSON response from the API.

        Raises:
            IntelliprintError: If the API returns an error response.
        """
        url = f"{self.BASE_URL}{endpoint}"

        headers = self._headers.copy()
        if files:
            # Remove Content-Type for multipart requests - requests will set it
            headers.pop("Content-Type", None)

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data if not files else None,
                data=json_data if files else None,
                files=files,
                timeout=self.TIMEOUT,
            )

            response_data = response.json()

            if not response.ok:
                error_info = response_data.get("error", {})
                raise IntelliprintError(
                    message=error_info.get("message", "Unknown error"),
                    error_type=error_info.get("type"),
                    error_code=error_info.get("code"),
                )

            return response_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Intelliprint API request failed: {e}")
            raise IntelliprintError(message=str(e), error_type="request_error") from e

    def _build_query_string(self, params: dict[str, Any]) -> str:
        """Build a query string from parameters.

        Args:
            params: Dictionary of query parameters.

        Returns:
            URL-encoded query string.
        """
        return "&".join(
            f"{k}={v}" for k, v in params.items() if v is not None
        )

