"""Address and recipient models for Intelliprint API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class IntelliprintAddress(BaseModel):
    """Address model for Intelliprint API.

    Represents a postal address for mail delivery.

    Attributes:
        name: The name of the recipient.
        line: The complete address line for the recipient (required).
        postcode: The postal code of the address.
        country: ISO 3166-1 alpha-2 country code (defaults to 'GB').
    """

    name: str | None = Field(default=None, description="The name of the recipient")
    line: str = Field(description="The complete address line for the recipient")
    postcode: str | None = Field(default=None, description="The postal code of the address")
    country: str = Field(default="GB", description="ISO 3166-1 alpha-2 country code")


class IntelliprintRecipient(BaseModel):
    """Recipient model for Intelliprint API.

    Represents a recipient with their address and optional template variables.

    Attributes:
        address: The address of the recipient.
        variables: Dynamic fields for template personalization.
    """

    address: IntelliprintAddress = Field(description="The address of the recipient")
    variables: dict[str, Any] | None = Field(
        default=None,
        description="Dynamic fields for templates (e.g., salutation, internal_id)"
    )

