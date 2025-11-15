# Implements functions to:
#  - read data from file (contacts + notes)
#  - save data back to file
#  - manage one JSON file (e.g., "assistant.json")


import json
from pathlib import Path
from typing import List, Tuple

from src.core.models.contacts import Contact
from src.core.models.notes import Note
from src.config.constants import DATA_FILE_NAME


class FileStore:
    """
    Simple JSON file store that keeps all data in a single file.

    The file contains a JSON object of the form:
        {
            "contacts": [...],
            "notes": [...]
        }

    Methods:
      - load()  -> (contacts: List[Contact], notes: List[Note])
      - save(contacts, notes) -> None
    """

    def __init__(self, file_path: Path | str | None = None) -> None:
        """
        Initialize the file store.

        Args:
            file_path: Optional custom path to the JSON file. If not provided,
                       a default file '.personal_assistant_data.json' in the
                       user's home directory is used.
        """
        if file_path is None:
            # Store data in user's home directory as required by the spec
            self.file_path = Path.home() / DATA_FILE_NAME
        else:
            self.file_path = Path(file_path)

    # -------- Internal helpers --------
    def _ensure_file(self) -> None:
        """Create the data file if it does not exist yet."""
        if not self.file_path.exists():
            self._write_raw({"contacts": [], "notes": []})

    def _read_raw(self) -> dict:
        """
        Read raw JSON data from the file.

        Returns a dict with at least 'contacts' and 'notes' keys.
        If the file is empty or corrupted, returns empty lists.
        """
        self._ensure_file()

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}

        data.setdefault("contacts", [])
        data.setdefault("notes", [])
        return data

    def _write_raw(self, data: dict) -> None:
        """Write raw JSON data to the file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # -------- Public API --------
    def load(self) -> Tuple[List[Contact], List[Note]]:
        """
        Load contacts and notes from disk.

        Returns:
            A tuple (contacts, notes) where each element is a list of
            corresponding model instances.
        """
        data = self._read_raw()

        contacts_data = data.get("contacts", [])
        notes_data = data.get("notes", [])

        contacts: List[Contact] = []
        for item in contacts_data:
            try:
                contacts.append(Contact.from_dict(item))
            except Exception:
                # Skip invalid records
                continue

        notes: List[Note] = []
        for item in notes_data:
            try:
                notes.append(Note.from_dict(item))
            except Exception:
                # Skip invalid records
                continue

        return contacts, notes

    def save(self, contacts: List[Contact], notes: List[Note]) -> None:
        """
        Persist contacts and notes to disk.

        Args:
            contacts: List of Contact instances to store
            notes: List of Note instances to store
        """
        data = {
            "contacts": [contact.to_dict() for contact in contacts],
            "notes": [note.to_dict() for note in notes],
        }
        self._write_raw(data)

    # Convenience methods to update only one entity type --------------
    def save_contacts(self, contacts: List[Contact]) -> None:
        """
        Persist only contacts, preserving existing notes on disk.
        """
        data = self._read_raw()
        data["contacts"] = [contact.to_dict() for contact in contacts]
        self._write_raw(data)

    def save_notes(self, notes: List[Note]) -> None:
        """
        Persist only notes, preserving existing contacts on disk.
        """
        data = self._read_raw()
        data["notes"] = [note.to_dict() for note in notes]
        self._write_raw(data)
