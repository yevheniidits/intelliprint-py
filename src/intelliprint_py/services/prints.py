"""Print jobs service for Intelliprint API."""

from __future__ import annotations

import base64
import logging
from typing import TYPE_CHECKING, Any, Literal

from intelliprint_py.models.address import IntelliprintAddress, IntelliprintRecipient
from intelliprint_py.models.enums import AddressWindow, PrintType
from intelliprint_py.models.settings import (
    BackgroundSettings,
    NudgeSettings,
    PostageSettings,
    PrintingSettings,
    SplittingSettings,
)
from intelliprint_py.models.user_data import UserData
from intelliprint_py.services.base import BaseService

if TYPE_CHECKING:
    from intelliprint_py.client import IntelliprintClient

logger = logging.getLogger(__name__)


class PrintsService(BaseService):
    """Service for managing print jobs.

    Print jobs are the core resource in the Intelliprint API. Each print job
    represents a collection of letters or postcards to be sent.

    Example:
        >>> client = IntelliprintClient(api_key="your-api-key")
        >>> print_job = client.prints.create(
        ...     content="Hello, World!",
        ...     recipients=[IntelliprintRecipient(
        ...         address=IntelliprintAddress(
        ...             name="John Doe",
        ...             line="123 Main St",
        ...             postcode="AB1 2CD"
        ...         )
        ...     )],
        ...     testmode=True
        ... )
    """

    def __init__(self, client: IntelliprintClient) -> None:
        """Initialize the prints service.

        Args:
            client: The parent IntelliprintClient instance.
        """
        super().__init__(client)

    def create(
        self,
        *,
        testmode: bool,
        content: str | None = None,
        template: str | None = None,
        file_content: bytes | None = None,
        file_name: str | None = None,
        file_url: str | None = None,
        recipients: list[IntelliprintRecipient] | None = None,
        user_data: UserData | None = None,
        mailing_list: str | None = None,
        print_type: PrintType = PrintType.LETTER,
        reference: str | None = None,
        confirmed: bool = False,
        printing: PrintingSettings | None = None,
        postage: PostageSettings | None = None,
        background: BackgroundSettings | None = None,
        splitting: SplittingSettings | None = None,
        nudge: NudgeSettings | None = None,
        confidential: bool = False,
        address_window: AddressWindow | None = None,
        confirmation_email: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new print job.

        You must explicitly specify testmode for every print job.

        Args:
            testmode: Whether to run in test mode (required). When True, your
                account is not charged and mail is not sent.
            content: Text or HTML content for the print job.
            template: ID of a pre-designed template to use.
            file_content: Binary content of a PDF/Word file.
            file_name: Name of the file when providing file_content.
            file_url: URL of a remote file to use.
            recipients: List of recipients to send the mail to.
            user_data: User data to use as the default recipient (if no
                recipients or mailing_list provided).
            mailing_list: ID of a mailing list to send to.
            print_type: Type of print job (letter or postcard).
            reference: User-friendly description for the print job.
            confirmed: Whether to confirm and submit for printing.
            printing: Printing settings (quality, color, double-sided).
            postage: Postage settings (service, envelope size, mail date).
            background: Background settings for letterheads.
            splitting: Settings for splitting multi-letter files.
            nudge: Settings for address positioning.
            confidential: Whether the print job is confidential.
            address_window: Position of the address window.
            confirmation_email: Whether to send a confirmation email.
            metadata: Arbitrary metadata to store with the print job.

        Returns:
            The created print job object from the API.

        Raises:
            IntelliprintError: If the API returns an error.
            ValueError: If user_data is required but not provided.
        """
        data: dict[str, Any] = {
            "type": print_type.value,
            "testmode": testmode,
            "confirmed": confirmed,
            "confidential": confidential,
            "confirmation_email": confirmation_email,
        }

        # Add content/template/file
        if content:
            data["content"] = content
        elif template:
            data["template"] = template
        elif file_content and file_name:
            data["file"] = {
                "content": base64.b64encode(file_content).decode("utf-8"),
                "name": file_name,
            }
        elif file_url:
            data["file"] = {"url": file_url}

        # Add recipients or mailing list
        if recipients:
            data["recipients"] = [r.model_dump(exclude_none=True) for r in recipients]
        elif mailing_list:
            data["mailing_list"] = mailing_list
        elif user_data:
            # Use user_data as default recipient
            data["recipients"] = [
                IntelliprintRecipient(
                    address=user_data.to_intelliprint_address(),
                    variables=user_data.to_template_variables(),
                ).model_dump(exclude_none=True)
            ]

        # Add optional settings
        if reference:
            data["reference"] = reference
        if printing:
            data["printing"] = printing.model_dump(exclude_none=True)
        if postage:
            data["postage"] = postage.model_dump(exclude_none=True)
        if background:
            data["background"] = background.model_dump(exclude_none=True)
        if splitting:
            data["splitting"] = splitting.model_dump(exclude_none=True)
        if nudge:
            data["nudge"] = nudge.model_dump(exclude_none=True)
        if address_window:
            data["address_window"] = address_window.value
        if metadata:
            data["metadata"] = metadata

        logger.info("Creating print job")
        return self._make_request("POST", "/prints", json_data=data)

    def get(self, print_id: str) -> dict[str, Any]:
        """Retrieve a print job by ID.

        Args:
            print_id: The ID of the print job to retrieve.

        Returns:
            The print job object from the API.
        """
        return self._make_request("GET", f"/prints/{print_id}")

    def list(
        self,
        *,
        limit: int = 10,
        skip: int = 0,
        testmode: bool = False,
        confirmed: bool | None = None,
        print_type: PrintType | None = None,
        reference: str | None = None,
        sort_field: str = "created",
        sort_order: Literal["asc", "desc"] = "desc",
    ) -> dict[str, Any]:
        """List print jobs with optional filtering.

        Args:
            limit: Number of objects to return (max 1000).
            skip: Number of objects to skip for pagination.
            testmode: Filter by test mode status.
            confirmed: Filter by confirmation status.
            print_type: Filter by print type.
            reference: Filter by exact reference.
            sort_field: Field to sort by.
            sort_order: Sort order (asc or desc).

        Returns:
            List object containing print jobs.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "skip": skip,
            "testmode": testmode,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }

        if confirmed is not None:
            params["confirmed"] = confirmed
        if print_type:
            params["type"] = print_type.value
        if reference:
            params["reference"] = reference

        query = self._build_query_string(params)
        return self._make_request("GET", f"/prints?{query}")

    def update(
        self,
        print_id: str,
        *,
        reference: str | None = None,
        testmode: bool | None = None,
        confirmed: bool | None = None,
        printing: PrintingSettings | None = None,
        postage: PostageSettings | None = None,
        background: BackgroundSettings | None = None,
        confidential: bool | None = None,
        address_window: AddressWindow | None = None,
        confirmation_email: bool | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a print job.

        Args:
            print_id: The ID of the print job to update.
            reference: New reference/description.
            testmode: Whether to run in test mode.
            confirmed: Whether to confirm the print job.
            printing: Updated printing settings.
            postage: Updated postage settings.
            background: Updated background settings.
            confidential: Whether the print job is confidential.
            address_window: Position of the address window.
            confirmation_email: Whether to send a confirmation email.
            metadata: Updated metadata.

        Returns:
            The updated print job object.
        """
        data: dict[str, Any] = {}

        if reference is not None:
            data["reference"] = reference
        if testmode is not None:
            data["testmode"] = testmode
        if confirmed is not None:
            data["confirmed"] = confirmed
        if printing:
            data["printing"] = printing.model_dump(exclude_none=True)
        if postage:
            data["postage"] = postage.model_dump(exclude_none=True)
        if background:
            data["background"] = background.model_dump(exclude_none=True)
        if confidential is not None:
            data["confidential"] = confidential
        if address_window:
            data["address_window"] = address_window.value
        if confirmation_email is not None:
            data["confirmation_email"] = confirmation_email
        if metadata is not None:
            data["metadata"] = metadata

        return self._make_request("POST", f"/prints/{print_id}", json_data=data)

    def confirm(self, print_id: str) -> dict[str, Any]:
        """Confirm a print job for printing.

        Once confirmed, the print job is submitted for printing and cannot
        be updated.

        Args:
            print_id: The ID of the print job to confirm.

        Returns:
            The confirmed print job object.
        """
        return self.update(print_id, confirmed=True)

    def delete(self, print_id: str) -> dict[str, Any]:
        """Delete or cancel a print job.

        For unconfirmed print jobs, this deletes them completely.
        For confirmed jobs, this attempts to cancel waiting_to_print items.

        Args:
            print_id: The ID of the print job to delete/cancel.

        Returns:
            The deletion result or updated print job object.
        """
        return self._make_request("DELETE", f"/prints/{print_id}")

