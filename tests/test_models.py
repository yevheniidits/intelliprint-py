"""Tests for models."""

import pytest

from intelliprint_py.models import (
    IntelliprintAddress,
    IntelliprintRecipient,
    UserAddress,
    UserData,
)


class TestIntelliprintAddress:
    """Tests for IntelliprintAddress model."""

    def test_create_minimal_address(self):
        """Test creating an address with only required fields."""
        address = IntelliprintAddress(line="123 Main St, London")
        assert address.line == "123 Main St, London"
        assert address.country == "GB"
        assert address.name is None
        assert address.postcode is None

    def test_create_full_address(self):
        """Test creating an address with all fields."""
        address = IntelliprintAddress(
            name="John Doe",
            line="123 Main St, London",
            postcode="SW1A 1AA",
            country="GB",
        )
        assert address.name == "John Doe"
        assert address.line == "123 Main St, London"
        assert address.postcode == "SW1A 1AA"
        assert address.country == "GB"


class TestUserData:
    """Tests for UserData model."""

    def test_create_user_data(self):
        """Test creating user data."""
        user = UserData(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john@example.com"
        assert user.extra == {}

    def test_user_data_full_name(self):
        """Test full_name property."""
        user = UserData(
            first_name="john",
            last_name="doe",
        )
        assert user.full_name == "John Doe"

    def test_user_data_with_extra(self):
        """Test creating user data with extra fields."""
        user = UserData(
            first_name="John",
            last_name="Doe",
            extra={"membership": "gold", "points": 100},
        )
        assert user.extra["membership"] == "gold"
        assert user.extra["points"] == 100

    def test_to_template_variables(self):
        """Test converting user data to template variables."""
        user = UserData(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            user_id="12345",
            extra={"custom_field": "value"},
        )
        variables = user.to_template_variables()

        assert variables["first_name"] == "John"
        assert variables["last_name"] == "Doe"
        assert variables["email"] == "john@example.com"
        assert variables["user_id"] == "12345"
        assert variables["custom_field"] == "value"

    def test_to_intelliprint_address(self):
        """Test converting user data to IntelliprintAddress."""
        user = UserData(
            first_name="John",
            last_name="Doe",
            address=[
                UserAddress(
                    building_number="123",
                    thoroughfare="Main Street",
                    post_town="London",
                    postcode="SW1A 1AA",
                )
            ],
        )
        address = user.to_intelliprint_address()

        assert address.name == "John Doe"
        assert "123" in address.line
        assert "Main Street" in address.line
        assert "London" in address.line
        assert address.postcode == "SW1A 1AA"
        assert address.country == "GB"

    def test_to_intelliprint_address_no_address(self):
        """Test error when converting user data without address."""
        user = UserData(
            first_name="John",
            last_name="Doe",
        )
        with pytest.raises(ValueError, match="No address available"):
            user.to_intelliprint_address()


class TestIntelliprintRecipient:
    """Tests for IntelliprintRecipient model."""

    def test_create_recipient(self):
        """Test creating a recipient."""
        recipient = IntelliprintRecipient(
            address=IntelliprintAddress(
                name="John Doe",
                line="123 Main St",
                postcode="SW1A 1AA",
            ),
            variables={"salutation": "Mr."},
        )
        assert recipient.address.name == "John Doe"
        assert recipient.variables == {"salutation": "Mr."}

    def test_recipient_model_dump(self):
        """Test dumping recipient to dict."""
        recipient = IntelliprintRecipient(
            address=IntelliprintAddress(
                name="John Doe",
                line="123 Main St",
            ),
        )
        data = recipient.model_dump(exclude_none=True)

        assert "address" in data
        assert data["address"]["name"] == "John Doe"
        assert "variables" not in data  # None values excluded

