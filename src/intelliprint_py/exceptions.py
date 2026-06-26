"""Custom exceptions for Intelliprint API."""

from __future__ import annotations


class IntelliprintError(Exception):
    """Exception raised for Intelliprint API errors.

    Attributes:
        message: Human-readable error message.
        error_type: The general category of the error.
        error_code: A unique code for the specific error.
    """

    def __init__(
        self,
        message: str,
        error_type: str | None = None,
        error_code: str | None = None,
    ) -> None:
        """Initialize IntelliprintError.

        Args:
            message: Human-readable error message.
            error_type: The general category of the error (e.g., 'invalid_request_error').
            error_code: A unique code for the specific error (e.g., 'parameter_invalid').
        """
        self.message = message
        self.error_type = error_type
        self.error_code = error_code
        super().__init__(self.message)

    def __repr__(self) -> str:
        return (
            f"IntelliprintError(message={self.message!r}, "
            f"error_type={self.error_type!r}, error_code={self.error_code!r})"
        )

