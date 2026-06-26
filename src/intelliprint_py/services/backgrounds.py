"""Backgrounds service for Intelliprint API."""

from __future__ import annotations

import base64
import logging
from typing import TYPE_CHECKING, Any, Literal

from intelliprint_py.services.base import BaseService

if TYPE_CHECKING:
    from intelliprint_py.client import IntelliprintClient

logger = logging.getLogger(__name__)


class BackgroundsService(BaseService):
    """Service for managing backgrounds (letterheads).

    Backgrounds allow you to apply reusable designs and artwork to your
    print jobs. Use them for letterheads, logos, and other recurring
    design elements.

    Note: This service does not require user data.

    Example:
        >>> client = IntelliprintClient(api_key="your-api-key")
        >>> with open("letterhead.pdf", "rb") as f:
        ...     background = client.backgrounds.create(
        ...         file_content=f.read(),
        ...         file_name="letterhead.pdf",
        ...         name="Company Letterhead"
        ...     )
    """

    def __init__(self, client: IntelliprintClient) -> None:
        """Initialize the backgrounds service.

        Args:
            client: The parent IntelliprintClient instance.
        """
        super().__init__(client)

    def create(
        self,
        file_content: bytes,
        file_name: str,
        name: str | None = None,
        team: str | None = None,
    ) -> dict[str, Any]:
        """Create a new background.

        Args:
            file_content: Binary content of the background PDF/Word file.
            file_name: Name of the file.
            name: User-friendly name for the background.
            team: Team ID to restrict usage to.

        Returns:
            The created background object.
        """
        data: dict[str, Any] = {
            "file": {
                "content": base64.b64encode(file_content).decode("utf-8"),
                "name": file_name,
            }
        }

        if name:
            data["name"] = name
        if team:
            data["team"] = team

        logger.info(f"Creating background: {name or file_name}")
        return self._make_request("POST", "/backgrounds", json_data=data)

    def get(self, background_id: str) -> dict[str, Any]:
        """Retrieve a background by ID.

        Args:
            background_id: The ID of the background to retrieve.

        Returns:
            The background object with a fresh signed PDF URL.
        """
        return self._make_request("GET", f"/backgrounds/{background_id}")

    def list(
        self,
        *,
        limit: int = 10,
        skip: int = 0,
        sort_field: Literal["created", "name"] = "created",
        sort_order: Literal["asc", "desc"] = "desc",
        team: str | None = None,
    ) -> dict[str, Any]:
        """List all backgrounds.

        Args:
            limit: Number of objects to return (max 1000).
            skip: Number of objects to skip for pagination.
            sort_field: Field to sort by.
            sort_order: Sort order (asc or desc).
            team: Filter by team ID.

        Returns:
            List object containing backgrounds.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "skip": skip,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }

        if team:
            params["team"] = team

        query = self._build_query_string(params)
        return self._make_request("GET", f"/backgrounds?{query}")

    def update(
        self,
        background_id: str,
        *,
        name: str | None = None,
        team: str | None = None,
    ) -> dict[str, Any]:
        """Update a background.

        Args:
            background_id: The ID of the background to update.
            name: New name for the background.
            team: New team ID restriction.

        Returns:
            The updated background object.
        """
        data: dict[str, Any] = {}

        if name is not None:
            data["name"] = name
        if team is not None:
            data["team"] = team

        return self._make_request("POST", f"/backgrounds/{background_id}", json_data=data)

    def delete(self, background_id: str) -> dict[str, Any]:
        """Delete a background.

        Note: Deletion fails if the background was used in any print job
        in the last 90 days.

        Args:
            background_id: The ID of the background to delete.

        Returns:
            Deletion confirmation object.
        """
        return self._make_request("DELETE", f"/backgrounds/{background_id}")

