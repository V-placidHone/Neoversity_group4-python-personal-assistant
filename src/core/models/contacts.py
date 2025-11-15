"""
Contact model module.

This module defines the Contact class and its helper classes for managing
contact information in the personal assistant application.
"""

from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime

from src.config.constants import default_date_format
from src.core.validators import is_phone, normalize_phone, is_email


class Field:
    """
    Base class for all record fields.

    This class serves as a foundation for specific field types like Name, Phone,
    Email, etc. It provides basic value storage and string representation.
    """

    def __init__(self, value: Any) -> None:
        """
        Initialize a field with a value.

        Args:
            value: The value to store in this field
        """
        self.value = value

    def __str__(self) -> str:
        """
        Return string representation of the field value.

        Returns:
            String representation of the stored value
        """
        return str(self.value)


class Name(Field):
    """
    Represents a contact's name.

    This class stores and validates contact names. Names are required fields
    and cannot be empty.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize a Name field.

        Args:
            value: The name string

        Raises:
            ValueError: If the name is empty or contains only whitespace
        """
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        super().__init__(value.strip())

    def __str__(self) -> str:
        """Return the name as a string."""
        return self.value


class Phone(Field):
    """
    Represents a contact's phone number.

    This class stores phone numbers. Basic validation can be added to ensure
    the phone number format is correct.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize a Phone field.

        Args:
            value: The phone number string

        Raises:
            ValueError: If the phone number is invalid
        """
        if not value or not value.strip():
            raise ValueError("Phone number cannot be empty")

        # Validate format (raises InvalidPhoneError on failure)
        is_phone(value.strip())

        # Normalize for storage
        cleaned_value = normalize_phone(value)
        super().__init__(cleaned_value)


class Email(Field):
    """
    Represents a contact's email address.

    This class stores email addresses with basic format validation.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize an Email field.

        Args:
            value: The email address string

        Raises:
            ValueError: If the email format is invalid
        """
        if not value or not value.strip():
            raise ValueError("Email cannot be empty")

        # Validate format (raises InvalidEmailError on failure)
        is_email(value.strip())

        super().__init__(value.strip().lower())


class Address(Field):
    """
    Represents a contact's physical address.

    This class stores full address information including street, city, state,
    and postal code.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize an Address field.

        Args:
            value: The address string
        """
        super().__init__(value.strip() if value else "")


class Birthday(Field):
    """
    Represents a contact's birthday.

    This class stores birthday information as a datetime object and provides
    methods for date formatting and validation.
    """

    def __init__(self, value: Optional[str] = None) -> None:
        """
        Initialize a Birthday field.

        Args:
            value: The birthday string in format 'DD.MM.YYYY' or 'YYYY-MM-DD'

        Raises:
            ValueError: If the date format is invalid
        """
        if value:
            try:
                # Try parsing DD.MM.YYYY format first
                if "." in value:
                    date_obj = datetime.strptime(value.strip(), default_date_format)
                # Try parsing YYYY-MM-DD format
                elif "-" in value:
                    date_obj = datetime.strptime(value.strip(), "%Y-%m-%d")
                else:
                    raise ValueError("Invalid date format")
                super().__init__(date_obj)
            except ValueError:
                raise ValueError(
                    "Invalid birthday format. Use DD.MM.YYYY or YYYY-MM-DD"
                )
        else:
            super().__init__(None)

    def __str__(self) -> str:
        """
        Return formatted birthday string.

        Returns:
            Birthday in DD.MM.YYYY format, or empty string if not set
        """
        if self.value:
            return self.value.strftime(default_date_format)
        return ""

    def get_date(self) -> Optional[datetime]:
        """
        Get the birthday as a datetime object.

        Returns:
            The birthday as a datetime object, or None if not set
        """
        return self.value


class Contact:
    """
    Main Contact class representing a person's contact information.

    This class manages all contact details including name, phone, email,
    address, and birthday. It provides methods for serialization and
    deserialization to/from dictionaries.
    """

    def __init__(
        self,
        name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        birthday: Optional[str] = None,
        contact_id: Optional[UUID] = None,
    ) -> None:
        """
        Initialize a Contact instance.

        Args:
            name: The contact's name (required)
            phone: The contact's phone number (optional)
            email: The contact's email address (optional)
            address: The contact's physical address (optional)
            birthday: The contact's birthday in DD.MM.YYYY or YYYY-MM-DD format (optional)
            contact_id: Unique identifier for the contact (optional, auto-generated if not provided)

        Raises:
            ValueError: If name is empty or any field validation fails
        """
        self.id: UUID = contact_id or self._generate_id()
        self.name: Name = Name(name)
        self.phone: Optional[Phone] = Phone(phone) if phone else None
        self.email: Optional[Email] = Email(email) if email else None
        self.address: Optional[Address] = Address(address) if address else None
        self.birthday: Optional[Birthday] = Birthday(birthday) if birthday else None

    def _generate_id(self) -> UUID:
        """
        Generate a unique ID for the contact.

        Returns:
            A unique identifier UUID using uuid4()
        """
        return uuid4()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the contact to a dictionary representation.

        This method serializes the contact object into a dictionary format
        suitable for JSON storage or API responses.

        Returns:
            Dictionary containing all contact fields with their values
        """
        return {
            "id": str(self.id),
            "name": str(self.name),
            "phone": str(self.phone) if self.phone else None,
            "email": str(self.email) if self.email else None,
            "address": str(self.address) if self.address else None,
            "birthday": str(self.birthday) if self.birthday else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Contact":
        """
        Create a Contact instance from a dictionary.

        This class method deserializes a dictionary into a Contact object,
        useful for loading contacts from JSON storage or API requests.

        Args:
            data: Dictionary containing contact field values

        Returns:
            A new Contact instance populated with the dictionary data

        Raises:
            KeyError: If required fields are missing from the dictionary
            ValueError: If any field validation fails
        """
        return cls(
            name=data["name"],
            phone=data.get("phone"),
            email=data.get("email"),
            address=data.get("address"),
            birthday=data.get("birthday"),
            contact_id=UUID(str(data.get("id"))) if data.get("id") else None,
        )

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the contact.

        This method formats the contact information in a clean, readable format
        suitable for display in the console or UI.

        Returns:
            Formatted string with all contact information
        """
        lines = [f"Contact ID: {str(self.id)}", f"Name: {self.name}"]

        if self.phone:
            lines.append(f"Phone: {self.phone}")

        if self.email:
            lines.append(f"Email: {self.email}")

        if self.address:
            lines.append(f"Address: {self.address}")

        if self.birthday:
            lines.append(f"Birthday: {self.birthday}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        """
        Return a detailed string representation for debugging.

        Returns:
            String representation showing the class name and key attributes
        """
        return (
            f"Contact(id='{str(self.id)}', name='{self.name}', "
            f"phone='{self.phone}', email='{self.email}')"
        )
