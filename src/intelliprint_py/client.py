"""Main client for Intelliprint API."""

from __future__ import annotations

import os

from intelliprint_py.services.backgrounds import BackgroundsService
from intelliprint_py.services.mailing_lists import MailingListsService
from intelliprint_py.services.prints import PrintsService


class IntelliprintClient:
    """Client for interacting with the Intelliprint API.

    This client provides access to all Intelliprint API services:
    - prints: Create and manage print jobs (letters and postcards)
    - backgrounds: Manage letterhead backgrounds
    - mailing_lists: Manage mailing lists and recipients

    Attributes:
        api_key: The API key for authentication.
        prints: Service for managing print jobs.
        backgrounds: Service for managing backgrounds.
        mailing_lists: Service for managing mailing lists.

    Example:
        >>> from intelliprint_py import IntelliprintClient, UserData, UserAddress
        >>>
        >>> # Initialize the client
        >>> client = IntelliprintClient(api_key="your-api-key")
        >>>
        >>> # Create a simple print job with HTML content
        >>> print_job = client.prints.create(
        ...     content="<h1>Hello World!</h1>",
        ...     testmode=True,
        ...     recipients=[IntelliprintRecipient(
        ...         address=IntelliprintAddress(
        ...             name="John Doe",
        ...             line="123 Main Street, London",
        ...             postcode="SW1A 1AA"
        ...         )
        ...     )]
        ... )
        >>>
        >>> # Or use UserData for more structured recipient info
        >>> user = UserData(
        ...     first_name="John",
        ...     last_name="Doe",
        ...     email="john@example.com",
        ...     address=[UserAddress(
        ...         building_number="123",
        ...         thoroughfare="Main Street",
        ...         post_town="London",
        ...         postcode="SW1A 1AA"
        ...     )],
        ...     extra={"customer_id": "12345"}
        ... )
        >>>
        >>> print_job = client.prints.create(
        ...     content="Dear {first_name}, welcome!",
        ...     testmode=True,
        ...     user_data=user
        ... )
    """

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize the Intelliprint client.

        Args:
            api_key: API key for authentication. If not provided, it will be
                read from the INTELLIPRINT_API_KEY environment variable.

        Raises:
            ValueError: If no API key is provided and the environment variable
                is not set.
        """
        self.api_key = api_key or os.getenv("INTELLIPRINT_API_KEY", "")

        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it as an argument or set the "
                "INTELLIPRINT_API_KEY environment variable."
            )

        # Initialize services
        self.prints = PrintsService(self)
        self.backgrounds = BackgroundsService(self)
        self.mailing_lists = MailingListsService(self)

    def __repr__(self) -> str:
        return f"IntelliprintClient(api_key='***')"

