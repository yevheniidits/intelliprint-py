"""Mailing lists service for Intelliprint API."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal

from intelliprint_py.models.address import IntelliprintAddress, IntelliprintRecipient
from intelliprint_py.models.user_data import UserData
from intelliprint_py.services.base import BaseService

if TYPE_CHECKING:
    from intelliprint_py.client import IntelliprintClient

logger = logging.getLogger(__name__)


class MailingListsService(BaseService):
    """Service for managing mailing lists and recipients.

    Mailing lists store groups of recipients, allowing you to send mail
    to multiple people with a single operation.

    Example:
        >>> client = IntelliprintClient(api_key="your-api-key")
        >>> mailing_list = client.mailing_lists.create(
        ...     name="Newsletter Subscribers"
        ... )
    """

    def __init__(self, client: IntelliprintClient) -> None:
        """Initialize the mailing lists service.

        Args:
            client: The parent IntelliprintClient instance.
        """
        super().__init__(client)

    # ============== Mailing Lists ==============

    def create(
        self,
        name: str,
        recipients: list[IntelliprintRecipient] | None = None,
        address_validation: bool = False,
    ) -> dict[str, Any]:
        """Create a new mailing list.

        Args:
            name: User-friendly name for the mailing list.
            recipients: Optional list of recipients to add.
            address_validation: Whether to request address validation.

        Returns:
            The created mailing list object.
        """
        data: dict[str, Any] = {"name": name}

        if recipients:
            data["recipients"] = [r.model_dump(exclude_none=True) for r in recipients]
        if address_validation:
            data["address_validation"] = {"requested": True}

        logger.info(f"Creating mailing list: {name}")
        return self._make_request("POST", "/mailing_lists", json_data=data)

    def get(self, mailing_list_id: str) -> dict[str, Any]:
        """Retrieve a mailing list by ID.

        Args:
            mailing_list_id: The ID of the mailing list to retrieve.

        Returns:
            The mailing list object.
        """
        return self._make_request("GET", f"/mailing_lists/{mailing_list_id}")

    def list(
        self,
        *,
        limit: int = 10,
        skip: int = 0,
        sort_field: Literal["created", "name", "recipients"] = "created",
        sort_order: Literal["asc", "desc"] = "desc",
    ) -> dict[str, Any]:
        """List all mailing lists.

        Args:
            limit: Number of objects to return (max 1000).
            skip: Number of objects to skip for pagination.
            sort_field: Field to sort by.
            sort_order: Sort order (asc or desc).

        Returns:
            List object containing mailing lists.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "skip": skip,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }

        query = self._build_query_string(params)
        return self._make_request("GET", f"/mailing_lists?{query}")

    def update(
        self,
        mailing_list_id: str,
        *,
        name: str | None = None,
        recipients: list[IntelliprintRecipient] | None = None,
        delete_old_recipients: bool = False,
        address_validation: bool | None = None,
    ) -> dict[str, Any]:
        """Update a mailing list.

        Args:
            mailing_list_id: The ID of the mailing list to update.
            name: New name for the mailing list.
            recipients: New recipients to add.
            delete_old_recipients: Whether to delete existing recipients first.
            address_validation: Whether to request address validation.

        Returns:
            The updated mailing list object.
        """
        data: dict[str, Any] = {}

        if name is not None:
            data["name"] = name
        if recipients:
            data["recipients"] = [r.model_dump(exclude_none=True) for r in recipients]
        if delete_old_recipients:
            data["delete_old_recipients"] = True
        if address_validation is not None:
            data["address_validation"] = {"requested": address_validation}

        return self._make_request("POST", f"/mailing_lists/{mailing_list_id}", json_data=data)

    def delete(self, mailing_list_id: str) -> dict[str, Any]:
        """Delete a mailing list and all its recipients.

        Args:
            mailing_list_id: The ID of the mailing list to delete.

        Returns:
            Deletion confirmation object.
        """
        return self._make_request("DELETE", f"/mailing_lists/{mailing_list_id}")

    # ============== Mailing List Recipients ==============

    def create_recipient(
        self,
        mailing_list_id: str,
        address: IntelliprintAddress,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new recipient in a mailing list.

        Args:
            mailing_list_id: The ID of the mailing list.
            address: The recipient's address.
            variables: Dynamic fields for templates.

        Returns:
            The created recipient object.
        """
        data: dict[str, Any] = {"address": address.model_dump(exclude_none=True)}

        if variables:
            data["variables"] = variables

        return self._make_request(
            "POST",
            f"/mailing_lists/{mailing_list_id}/recipients",
            json_data=data
        )

    def get_recipient(self, mailing_list_id: str, recipient_id: str) -> dict[str, Any]:
        """Retrieve a recipient from a mailing list.

        Args:
            mailing_list_id: The ID of the mailing list.
            recipient_id: The ID of the recipient.

        Returns:
            The recipient object.
        """
        return self._make_request(
            "GET",
            f"/mailing_lists/{mailing_list_id}/recipients/{recipient_id}"
        )

    def list_recipients(
        self,
        mailing_list_id: str,
        *,
        limit: int = 10,
        skip: int = 0,
        sort_field: Literal["created", "name"] = "created",
        sort_order: Literal["asc", "desc"] = "desc",
    ) -> dict[str, Any]:
        """List all recipients in a mailing list.

        Args:
            mailing_list_id: The ID of the mailing list.
            limit: Number of objects to return (max 1000).
            skip: Number of objects to skip for pagination.
            sort_field: Field to sort by.
            sort_order: Sort order (asc or desc).

        Returns:
            List object containing recipients.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "skip": skip,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }

        query = self._build_query_string(params)
        return self._make_request(
            "GET",
            f"/mailing_lists/{mailing_list_id}/recipients?{query}"
        )

    def update_recipient(
        self,
        mailing_list_id: str,
        recipient_id: str,
        *,
        address: IntelliprintAddress | None = None,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a recipient in a mailing list.

        Args:
            mailing_list_id: The ID of the mailing list.
            recipient_id: The ID of the recipient.
            address: Updated address.
            variables: Updated dynamic fields.

        Returns:
            The updated recipient object.
        """
        data: dict[str, Any] = {}

        if address:
            data["address"] = address.model_dump(exclude_none=True)
        if variables is not None:
            data["variables"] = variables

        return self._make_request(
            "POST",
            f"/mailing_lists/{mailing_list_id}/recipients/{recipient_id}",
            json_data=data
        )

    def delete_recipient(self, mailing_list_id: str, recipient_id: str) -> dict[str, Any]:
        """Delete a recipient from a mailing list.

        Args:
            mailing_list_id: The ID of the mailing list.
            recipient_id: The ID of the recipient.

        Returns:
            Deletion confirmation object.
        """
        return self._make_request(
            "DELETE",
            f"/mailing_lists/{mailing_list_id}/recipients/{recipient_id}"
        )

    def add_user(
        self,
        mailing_list_id: str,
        user_data: UserData,
        additional_variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Add a user to a mailing list - convenience method.

        This method takes a UserData object and adds it as a recipient
        to the specified mailing list, automatically converting the
        user data to the required format.

        Args:
            mailing_list_id: The ID of the mailing list.
            user_data: The user data to add.
            additional_variables: Additional template variables to include.

        Returns:
            The created recipient object.
        """
        variables = user_data.to_template_variables()

        if additional_variables:
            variables.update(additional_variables)

        return self.create_recipient(
            mailing_list_id=mailing_list_id,
            address=user_data.to_intelliprint_address(),
            variables=variables,
        )

