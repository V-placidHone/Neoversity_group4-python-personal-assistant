"""
Service layer for managing contacts.

This module provides the ContactsService class which handles all CRUD operations
(Create, Read, Update, Delete) for contacts, including validation and search functionality.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID


from src.core.models.contacts import Contact
from src.core.errors import (
    ContactNotFoundError,
    DuplicateContactError,
)
from src.storage import default_store


class ContactsService:
    """
    Service class for managing contact operations.

    This class provides a high-level interface for contact management,
    handling validation, storage operations, and business logic.
    """

    def __init__(self, store: Any | None = None) -> None:
        """
        Initialize the ContactsService with a storage backend.

        Args:
            store: Storage backend that implements load() and save() methods
                   Expected interface:
                   - load() -> (contacts: List[Contact], notes: List[Note])
                   - save(contacts: List[Contact], notes: List[Note]) -> None
                   If not provided, a shared default_store is used.
        """
        # Use shared default_store if no explicit store provided
        self.store = store or default_store
        self._contacts: List[Contact] = []
        self._load_contacts()

    def _load_contacts(self) -> None:
        """
        Load contacts from the storage backend.

        This is called during initialization to populate the in-memory contact list.
        """
        try:
            contacts, _ = self.store.load()
            self._contacts = contacts if contacts else []
        except Exception:
            # If loading fails (e.g., file doesn't exist), start with empty list
            self._contacts = []

    def _save_contacts(self) -> None:
        """
        Save contacts to the storage backend.

        This persists the current in-memory contact list to storage.
        """
        # Delegate persistence details to the store implementation
        self.store.save_contacts(self._contacts)

    def get_all(self) -> List[Contact]:
        """
        Retrieve all contacts.

        Returns:
            List of all Contact objects in the system
        """
        return self._contacts.copy()

    def add(self, contact_data: Dict[str, Any]) -> Contact:
        """
        Add a new contact to the system.

        Validates all fields before adding and checks for duplicate names.

        Args:
            contact_data: Dictionary containing contact information
                         Required: 'name'
                         Optional: 'phone', 'email', 'address', 'birthday'

        Returns:
            The newly created Contact object

        Raises:
            ValidationError: If any field fails validation
            DuplicateContactError: If a contact with the same name already exists
        """
        # Check if contact with this name already exists
        name = contact_data.get("name", "").strip()
        if self._find_by_name(name):
            raise DuplicateContactError(name)

        # Create new contact (validation happens in Contact.__init__)
        new_contact = Contact(
            name=contact_data.get("name"),
            phone=contact_data.get("phone"),
            email=contact_data.get("email"),
            address=contact_data.get("address"),
            birthday=contact_data.get("birthday"),
        )

        # Add to list and save
        self._contacts.append(new_contact)
        self._save_contacts()

        return new_contact

    def update(self, contact_id: UUID, contact_data: Dict[str, Any]) -> Contact:
        """
        Completely update an existing contact (replace all fields).

        This method replaces all fields of the contact with new values.
        Any field not provided in contact_data will be set to None/empty.

        Args:
            contact_id: Unique identifier of the contact to update
            contact_data: Dictionary containing new contact information
                         Required: 'name'
                         Optional: 'phone', 'email', 'address', 'birthday'

        Returns:
            The updated Contact object

        Raises:
            ContactNotFoundError: If no contact with the given ID exists
            ValidationError: If any field fails validation
        """
        # Find the contact
        contact = self._find_by_id(contact_id)
        if not contact:
            raise ContactNotFoundError(contact_id)

        # Check if new name conflicts with another contact
        new_name = contact_data.get("name", "").strip()
        existing = self._find_by_name(new_name)
        if existing and existing.id != contact_id:
            raise DuplicateContactError(new_name)

        # Create a new contact with updated data (preserving the ID)
        updated_contact = Contact(
            name=contact_data.get("name"),
            phone=contact_data.get("phone"),
            email=contact_data.get("email"),
            address=contact_data.get("address"),
            birthday=contact_data.get("birthday"),
            contact_id=contact_id,
        )

        # Replace the old contact with the updated one
        index = self._contacts.index(contact)
        self._contacts[index] = updated_contact
        self._save_contacts()

        return updated_contact

    def patch(self, contact_id: UUID, updates: Dict[str, Any]) -> Contact:
        """
        Partially update an existing contact (update only specified fields).

        This method updates only the fields provided in the updates dictionary,
        leaving other fields unchanged.

        Args:
            contact_id: Unique identifier of the contact to update
            updates: Dictionary containing fields to update
                    Possible keys: 'name', 'phone', 'email', 'address', 'birthday'

        Returns:
            The updated Contact object

        Raises:
            ContactNotFoundError: If no contact with the given ID exists
            ValidationError: If any field fails validation
        """
        # Find the contact
        contact = self._find_by_id(contact_id)
        if not contact:
            raise ContactNotFoundError(contact_id)

        # Check if name update conflicts with another contact
        if "name" in updates:
            new_name = updates["name"].strip()
            existing = self._find_by_name(new_name)
            if existing and existing.id != contact_id:
                raise DuplicateContactError(new_name)

        # Update individual fields using the contact's update methods
        if "name" in updates:
            contact.name.value = updates["name"].strip()

        if "phone" in updates:
            if updates["phone"]:
                contact.phone.value = updates["phone"].strip()
            else:
                contact.phone = None

        if "email" in updates:
            if updates["email"]:
                contact.email.value = updates["email"].strip()
            else:
                contact.email = None

        if "address" in updates:
            contact.address.value = updates["address"].strip() or ""

        if "birthday" in updates:
            if updates["birthday"]:
                contact.birthday.value = updates["birthday"].strip()
            else:
                contact.birthday.value = None

        # Save changes
        self._save_contacts()

        return contact

    def delete(self, contact_id: UUID) -> bool:
        """
        Delete a contact from the system.

        Args:
            contact_id: Unique identifier of the contact to delete

        Returns:
            True if the contact was successfully deleted

        Raises:
            ContactNotFoundError: If no contact with the given ID exists
        """
        # Find the contact
        contact = self._find_by_id(contact_id)
        if not contact:
            raise ContactNotFoundError(contact_id)

        # Remove from list and save
        self._contacts.remove(contact)
        self._save_contacts()

        return True

    def search(
        self,
        query: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
    ) -> List[Contact]:
        """
        Search for contacts based on various criteria.

        Supports searching by:
        - General query (searches across name, phone, email, address)
        - Specific field matching (name, phone, email)

        All searches are case-insensitive and support partial matching.

        Args:
            query: General search term to match against all fields
            name: Specific name to search for
            phone: Specific phone number to search for
            email: Specific email to search for

        Returns:
            List of Contact objects matching the search criteria
        """
        results = []

        for contact in self._contacts:
            # If general query is provided, search across all fields
            if query:
                query_lower = query.lower()
                if (
                    query_lower in contact.name.value.lower()
                    or (contact.phone and query_lower in contact.phone.value.lower())
                    or (contact.email and query_lower in contact.email.value.lower())
                    or (
                        contact.address and query_lower in contact.address.value.lower()
                    )
                ):
                    results.append(contact)
                    continue

            # Check specific field criteria
            match = True

            if name and name.lower() not in contact.name.value.lower():
                match = False

            if phone and contact.phone and phone not in contact.phone.value.lower():
                match = False

            if (
                email
                and contact.email
                and email.lower() not in contact.email.value.lower()
            ):
                match = False

            if match and (name or phone or email):
                results.append(contact)

        return results

    def get_by_id(self, contact_id: UUID) -> Optional[Contact]:
        """
        Retrieve a contact by its unique ID.

        Args:
            contact_id: Unique identifier of the contact

        Returns:
            The Contact object if found, None otherwise
        """
        return self._find_by_id(contact_id)

    def _find_by_id(self, contact_id: UUID) -> Optional[Contact]:
        """
        Internal helper method to find a contact by ID.

        Args:
            contact_id: Unique identifier of the contact

        Returns:
            The Contact object if found, None otherwise
        """
        for contact in self._contacts:
            if contact.id == contact_id:
                return contact
        return None

    def _find_by_name(self, name: str) -> Optional[Contact]:
        """
        Internal helper method to find a contact by exact name match.

        Args:
            name: Name to search for (case-insensitive)

        Returns:
            The Contact object if found, None otherwise
        """
        name_lower = name.lower()
        for contact in self._contacts:
            if contact.name.value.lower() == name_lower:
                return contact
        return None
