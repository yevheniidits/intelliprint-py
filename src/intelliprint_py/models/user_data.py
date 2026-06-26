"""User data model for Intelliprint API.

This module provides a simple, flexible model for user/recipient data
that can be passed to methods requiring user information.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from intelliprint_py.models.address import IntelliprintAddress


class UserAddress(BaseModel):
    """User address model with common address components.

    Attributes:
        building_number: The building number.
        building_name: The building name.
        thoroughfare: The street/thoroughfare.
        post_town: The post town/city.
        county: The county/region.
        postcode: The postal code.
        country: The country (defaults to 'GB').
    """

    building_number: str | None = Field(default=None, description="The building number")
    building_name: str | None = Field(default=None, description="The building name")
    thoroughfare: str | None = Field(default=None, description="The street/thoroughfare")
    post_town: str | None = Field(default=None, description="The post town/city")
    county: str | None = Field(default=None, description="The county/region")
    postcode: str | None = Field(default=None, description="The postal code")
    country: str = Field(default="GB", description="ISO 3166-1 alpha-2 country code")


class UserData(BaseModel):
    """User data model for methods that require recipient information.

    This is a simple, flexible model for providing user/lead data to
    Intelliprint API methods. It includes basic required fields and
    an `extra` dictionary for any additional data you want to include
    as template variables.

    Attributes:
        first_name: The user's first name.
        last_name: The user's last name.
        email: The user's email address (optional).
        address: The user's address (optional, can be a list for multiple addresses).
        user_id: An optional identifier for the user (e.g., lead_id, customer_id).
        extra: Additional data to include as template variables.

    Example:
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
        ...     extra={"membership_level": "gold", "account_number": "12345"}
        ... )
    """

    first_name: str = Field(description="The user's first name")
    last_name: str = Field(description="The user's last name")
    email: str | None = Field(default=None, description="The user's email address")
    address: list[UserAddress] | None = Field(
        default=None,
        description="The user's address(es)"
    )
    user_id: str | None = Field(
        default=None,
        description="An optional identifier for the user"
    )
    extra: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional data to include as template variables"
    )

    # Country code mapping for common country names
    COUNTRY_MAPPING: dict[str, str] = {
        "England": "GB",
        "Scotland": "GB",
        "Wales": "GB",
        "Northern Ireland": "GB",
        "United Kingdom": "GB",
        "United States": "US",
        "USA": "US",
    }

    @property
    def full_name(self) -> str:
        """Get the user's full name with proper title case.

        Returns:
            The full name formatted as 'First Last'.
        """
        return f"{self.first_name.title()} {self.last_name.title()}".strip()

    def to_intelliprint_address(self) -> IntelliprintAddress:
        """Convert user data to an IntelliprintAddress.

        Uses the first address in the address list if available.

        Returns:
            IntelliprintAddress with the user's address information.

        Raises:
            ValueError: If no address is available.
        """
        if not self.address:
            raise ValueError("No address available for user")

        primary_address = self.address[0]

        # Build address line from components
        address_parts = []
        for field in ["building_number", "building_name", "thoroughfare", "post_town", "county"]:
            value = getattr(primary_address, field, None)
            if value:
                address_parts.append(str(value))

        address_line = ", ".join(filter(None, address_parts))
        postcode = primary_address.postcode
        country = self.COUNTRY_MAPPING.get(primary_address.country, primary_address.country)

        return IntelliprintAddress(
            name=self.full_name,
            line=address_line,
            postcode=postcode,
            country=country,
        )

    def to_template_variables(self) -> dict[str, Any]:
        """Get all user data as template variables.

        Returns:
            Dictionary containing user_id, first_name, last_name, email,
            and any extra data provided.
        """
        variables: dict[str, Any] = {
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

        if self.user_id:
            variables["user_id"] = self.user_id
        if self.email:
            variables["email"] = self.email

        # Merge extra data
        variables.update(self.extra)

        return variables

