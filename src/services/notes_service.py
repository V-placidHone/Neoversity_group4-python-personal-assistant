# Handles CRUD for notes:
#  - add(), delete(), find(), find_by_tags(), edit()
#  - each note may include one or more tags


# services/notes_service.py

# services/notes_service.py

from core.models.notes import Note
from storage.file_store import FileStore  # assuming this is your storage class

class NotesService:
    def __init__(self, store=None):
        """
        store: storage object (e.g., FileStore). Optional, defaults to in-memory list.
        """
        self.store = store or FileStore()
        self.notes = self.store.load()  # load existing notes from storage

    def get_all(self):
        return self.notes

    def add(self, note):
        if not isinstance(note, Note):
            raise ValueError("Expected a Note object")
        self.notes.append(note)
        self.store.save(self.notes)
        return note

    def update(self, note_id, **kwargs):
        note = self.find(note_id)
        if not note:
            raise ValueError(f"Note with id {note_id} not found")
        note.text = kwargs.get("text", note.text)
        note.tags = kwargs.get("tags", note.tags)
        self.store.save(self.notes)
        return note

    def delete(self, note_id):
        note = self.find(note_id)
        if not note:
            raise ValueError(f"Note with id {note_id} not found")
        self.notes.remove(note)
        self.store.save(self.notes)
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
            results = [note for note in results if tags_set.intersection(t.lower() for t in note.tags)]
        if text:
            text_lower = text.lower()
            results = [note for note in results if text_lower in note.text.lower()]
        return results


    




