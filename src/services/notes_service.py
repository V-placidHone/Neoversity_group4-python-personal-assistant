from typing import Any
from src.core.models.notes import Note
from src.storage import default_store


class NotesService:
    def __init__(self, store: Any | None = None) -> None:
        """
        store: storage object (e.g., FileStore). Optional, defaults to in-memory list.
        """
        # Use shared default_store if no explicit store provided
        self.store = store or default_store
        _, notes = self.store.load()
        self.notes = notes

    def get_all(self):
        return self.notes

    def add(self, note):
        if not isinstance(note, Note):
            raise ValueError("Expected a Note object")
        self.notes.append(note)
        # Store is responsible for preserving other entity types
        self.store.save_notes(self.notes)
        return note

    def update(self, note_id, **kwargs):
        note = self.find(note_id)
        if not note:
            raise ValueError(f"Note with id {note_id} not found")
        note.text = kwargs.get("text", note.text)
        note.tags = kwargs.get("tags", note.tags)
        self.store.save_notes(self.notes)
        return note

    def delete(self, note_id):
        note = self.find(note_id)
        if not note:
            raise ValueError(f"Note with id {note_id} not found")
        self.notes.remove(note)
        self.store.save_notes(self.notes)
        return True

    def find(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def find_by_tags(self, tags=None, text=None):
        results = self.notes
        if tags:
            tags_set = set(tag.lower() for tag in tags)
            results = [
                note
                for note in results
                if tags_set.intersection(t.lower() for t in note.tags)
            ]
        if text:
            text_lower = text.lower()
            results = [note for note in results if text_lower in note.text.lower()]
        return results
