"""
Business logic layer — connects models with storage.

Re-export service classes for convenient imports, e.g.:

    from src.services import ContactsService, NotesService
"""

from .contacts_service import ContactsService
from .notes_service import NotesService
from .birthday_service import BirthdayService
from .search_service import SearchService

__all__ = [
    "ContactsService",
    "NotesService",
    "BirthdayService",
    "SearchService",
]
