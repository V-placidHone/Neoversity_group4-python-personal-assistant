"""
Validation functions for contact data fields.

This module provides validation and parsing functions for email addresses,
phone numbers, and birthday dates. These validators ensure data integrity
before storing contact information.
"""

import re
from datetime import datetime
from typing import Optional

from .errors import InvalidEmailError, InvalidPhoneError, InvalidBirthdayError
from src.config.constants import email_pattern


def is_email(value: str) -> bool:
    """
    Validate an email address format.

    Checks if the provided string matches a valid email format using regex.
    The validation ensures the email has a local part, @ symbol, and domain.

    Args:
        value: The email string to validate

    Returns:
        True if the email format is valid, False otherwise

    Raises:
        InvalidEmailError: If the email format is invalid
    """
    if not value or not isinstance(value, str):
        raise InvalidEmailError(str(value))

    if not re.match(email_pattern, value.strip()):
        raise InvalidEmailError(value)

    return True


def is_phone(value: str) -> bool:
    """
    Validate a phone number format.

    Checks if the provided string contains exactly 10 digits.
    Strips common formatting characters (spaces, dashes, parentheses, plus signs)
    before validation.

    Args:
        value: The phone number string to validate

    Returns:
        True if the phone format is valid, False otherwise

    Raises:
        InvalidPhoneError: If the phone format is invalid
    """
    if not value or not isinstance(value, str):
        raise InvalidPhoneError(str(value))

    # Remove common phone number formatting characters
    cleaned = re.sub(r"[\s\-\(\)\+]", "", value.strip())

    # Check if the result contains exactly 10 digits
    if not re.match(r"^\d{10}$", cleaned):
        raise InvalidPhoneError(value)

    return True


def parse_birthday(value: str) -> Optional[datetime]:
    """
    Parse a birthday string into a datetime object.

    Attempts to parse the birthday using multiple common date formats:
    - DD.MM.YYYY (European format)
    - YYYY-MM-DD (ISO format)
    - DD/MM/YYYY (Alternative format)
    - MM/DD/YYYY (US format)

    Also validates that the date is not in the future and represents
    a reasonable age (not more than 150 years ago).

    Args:
        value: The birthday string to parse

    Returns:
        A datetime object representing the birthday, or None if parsing fails

    Raises:
        InvalidBirthdayError: If the date format is invalid or date is unrealistic
    """
    if not value or not isinstance(value, str):
        raise InvalidBirthdayError(str(value), "Birthday must be a non-empty string")

    value = value.strip()

    # List of date formats to try, in order of preference
    date_formats = [
        "%d.%m.%Y",  # DD.MM.YYYY (European)
        "%Y-%m-%d",  # YYYY-MM-DD (ISO)
        "%d/%m/%Y",  # DD/MM/YYYY
        "%m/%d/%Y",  # MM/DD/YYYY (US)
    ]

    parsed_date = None

    # Try each format until one succeeds
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(value, date_format)
            break
        except ValueError:
            continue

    # If no format matched, raise an error
    if parsed_date is None:
        raise InvalidBirthdayError(
            value,
            "Could not parse date. Supported formats: DD.MM.YYYY, YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY",
        )

    # Validate that the date is not in the future
    current_date = datetime.now()
    if parsed_date > current_date:
        raise InvalidBirthdayError(value, "Birthday cannot be in the future")

    # Validate that the date is not more than 150 years ago (reasonable age limit)
    max_age_years = 150
    min_date = datetime(current_date.year - max_age_years, 1, 1)
    if parsed_date < min_date:
        raise InvalidBirthdayError(
            value, f"Birthday cannot be more than {max_age_years} years ago"
        )

    return parsed_date


def normalize_phone(value: str) -> str:
    """
    Normalize a phone number to a standard format.

    Removes all formatting characters and returns just the digits.
    This is useful for storing phone numbers in a consistent format.

    Args:
        value: The phone number string to normalize

    Returns:
        A string containing only the digits of the phone number
    """
    return re.sub(r"[\s\-\(\)\+]", "", value.strip())


def format_phone(value: str) -> str:
    """
    Format a phone number for display.

    Takes a normalized phone number (10 digits) and formats it
    in a readable format: (XXX) XXX-XXXX

    Args:
        value: The phone number string to format (should be 10 digits)

    Returns:
        A formatted phone number string
    """
    if len(value) == 10:
        return f"({value[:3]}) {value[3:6]}-{value[6:]}"
    return value
