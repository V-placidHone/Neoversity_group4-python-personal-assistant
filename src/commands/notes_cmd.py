from uuid import UUID

from ..services.notes_service import NotesService
from src.core.models.notes import Note, Text, Tag
from src.config.constants import (
    NOTES_SEARCH_RESULT_TRUNCATE,
    NOTES_LIST_RESULT_TRUNCATE,
)


class NotesCommand:
    def __init__(self):
        self.service = NotesService()

    def add_note(self, text, tags=None):
        try:
            if not text or not text.strip():
                return "Error: Note text cannot be empty"

            note_text = Text(text.strip())
            note_tags = [Tag(t) for t in (tags or [])]
            note = Note(text=note_text, tags=note_tags)

            result = self.service.add(note)
            tag_info = f" with tags: {', '.join(tags)}" if tags else ""
            return f"Note successfully added! (ID: {result.id}){tag_info}"
        except Exception as e:
            return f"Error adding note: {str(e)}"

    def edit_note(self, note_id, new_text=None, new_tags=None):
        try:
            note_uuid = UUID(str(note_id))
            updates = {}
            if new_text is not None:
                updates["text"] = Text(new_text)
            if new_tags is not None:
                updates["tags"] = [Tag(t) for t in new_tags]

            self.service.update(note_uuid, **updates)
            return f"Note (ID: {note_id}) successfully updated!"
        except Exception as e:
            return f"Error editing note: {str(e)}"

    def delete_note(self, note_id):
        try:
            note_uuid = UUID(str(note_id))
            self.service.delete(note_uuid)
            return f"Note (ID: {note_id}) successfully deleted!"
        except Exception as e:
            return f"Error deleting note: {str(e)}"

    def search_notes(self, query):
        try:
            results = self.service.find_by_tags(text=query)
            if not results:
                return f"No notes found for query '{query}'"

            output = ["Note search results:"]
            for note in results:
                truncated_text = self._truncate_text(
                    note.text, NOTES_SEARCH_RESULT_TRUNCATE
                )
                note_info = f"{truncated_text}"
                if note.tags:
                    note_info += (
                        " | Tags: " + ", ".join(str(tag) for tag in note.tags)
                    )
                note_info += f" | ID: {note.id}"
                output.append(note_info)

            return "\n".join(output)
        except Exception as e:
            return f"Error searching notes: {str(e)}"

    def search_notes_by_tag(self, tag):
        try:
            results = self.service.find_by_tags(tags=[tag])
            if not results:
                return f"No notes found with tag '{tag}'"

            output = [f"Notes with tag '{tag}':"]
            for note in results:
                truncated_text = self._truncate_text(
                    note.text, NOTES_SEARCH_RESULT_TRUNCATE
                )
                note_info = f"{truncated_text}"
                if note.tags:
                    note_info += (
                        " | Tags: " + ", ".join(str(tag) for tag in note.tags)
                    )
                note_info += f" | ID: {note.id}"
                output.append(note_info)

            return "\n".join(output)
        except Exception as e:
            return f"Error searching by tag: {str(e)}"

    def list_notes(self):
        try:
            notes = self.service.get_all()
            if not notes:
                return "Note list is empty"

            output = ["All notes:"]
            for note in notes:
                truncated_text = self._truncate_text(
                    note.text, NOTES_LIST_RESULT_TRUNCATE
                )
                note_info = f"{truncated_text}"
                if note.tags:
                    note_info += (
                        " | Tags: " + ", ".join(str(tag) for tag in note.tags)
                    )
                note_info += f" | ID: {note.id}"
                output.append(note_info)

            return "\n".join(output)
        except Exception as e:
            return f"Error getting note list: {str(e)}"

    def _truncate_text(self, text, max_length):
        if len(text) <= max_length:
            return text
        return text[:max_length] + "...."
