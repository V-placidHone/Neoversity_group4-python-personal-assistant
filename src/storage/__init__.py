"""
Handles persistent data storage (read/write to disk).

Re-export FileStore and a shared default_store for convenient imports:

    from src.storage import FileStore, default_store
"""

from .file_store import FileStore

# Single shared store instance for the whole application.
# All services should use this instance by default to avoid
# creating multiple independent stores.
default_store = FileStore()

__all__ = ["FileStore", "default_store"]
