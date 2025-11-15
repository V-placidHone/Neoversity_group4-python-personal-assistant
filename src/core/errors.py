"""
Custom exceptions for domain errors in the personal assistant application.

This module defines specific exception classes for validation and business logic errors,
making error handling more precise and informative throughout the application.
"""

from typing import Optional
from uuid import UUID


class ValidationError(Exception):
    """
    Base exception class for all validation-related errors.

    This serves as a parent class for more specific validation exceptions,
    allowing for broad exception handling when needed.
    """

    def __init__(self, message: str, field_name: Optional[str] = None) -> None:
        """
        Initialize the validation error.

        Args:
            message: A descriptive error message explaining what went wrong
            field_name: Optional name of the field that failed validation
        """
        self.field_name = field_name
        super().__init__(message)


class InvalidEmailError(ValidationError):
    """
    Exception raised when an email address fails validation.

    This is raised when an email doesn't match the expected format
    or contains invalid characters.
    """

    def __init__(self, email: str) -> None:
        """
        Initialize the invalid email error.

        Args:
            email: The email address that failed validation
        """
        super().__init__(
            f"Invalid email format: '{email}'. Expected format: user@domain.com",
            field_name="email",
        )
        self.email = email


class InvalidPhoneError(ValidationError):
    """
    Exception raised when a phone number fails validation.

    This is raised when a phone number doesn't match the expected format
    or contains invalid characters.
    """

    def __init__(self, phone: str) -> None:
        """
        Initialize the invalid phone error.

        Args:
            phone: The phone number that failed validation
        """
        super().__init__(
            f"Invalid phone format: '{phone}'. Expected format: 10 digits (e.g., 1234567890)",
            field_name="phone",
        )
        self.phone = phone


class InvalidBirthdayError(ValidationError):
    """
    Exception raised when a birthday date fails validation or parsing.

    This is raised when a birthday string cannot be parsed into a valid date
    or represents an invalid date (e.g., future date, unrealistic age).
    """

    def __init__(self, birthday: str, reason: Optional[str] = None) -> None:
        """
        Initialize the invalid birthday error.

        Args:
            birthday: The birthday string that failed validation
            reason: Optional specific reason for the validation failure
        """
        message = f"Invalid birthday: '{birthday}'"
        if reason:
            message += f". {reason}"
        else:
            message += ". Expected format: DD.MM.YYYY or YYYY-MM-DD"

        super().__init__(message, field_name="birthday")
        self.birthday = birthday


class ContactNotFoundError(Exception):
    """
    Exception raised when a requested contact cannot be found.

    This is typically raised during update, delete, or search operations
    when the specified contact ID or name doesn't exist in the storage.
    """

    def __init__(self, identifier: UUID) -> None:
        """
        Initialize the contact not found error.

        Args:
            identifier: The ID or name of the contact that wasn't found
        """
        super().__init__(f"Contact not found: '{str(identifier)}'")
        self.identifier = identifier


class DuplicateContactError(Exception):
    """
    Exception raised when attempting to add a contact that already exists.

    This helps prevent duplicate entries in the contact list.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the duplicate contact error.

        Args:
            name: The name of the contact that already exists
        """
        super().__init__(f"Contact with name '{name}' already exists")
        self.name = name
