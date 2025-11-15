"""
Data models (represent contacts and notes as Python objects).

Re-exports common model classes for convenient imports, e.g.:

    from src.core.models import Contact, Note
"""

from .contacts import Contact
from .notes import Note, Text, Tag

__all__ = ["Contact", "Note", "Text", "Tag"]
