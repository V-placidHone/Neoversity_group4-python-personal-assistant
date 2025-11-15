from ..services.notes_service import NotesService

class NotesCommand:
    # Constants for text truncation
    SEARCH_RESULT_TRUNCATE = 80
    LIST_RESULT_TRUNCATE = 60
    GLOBAL_SEARCH_TRUNCATE = 100
    
    def __init__(self):
        self.service = NotesService()
    
    def add_note(self, text, tags=None):
        try:
            if not text or not text.strip():
                return "Error: Note text cannot be empty"
            
            result = self.service.add_note(text.strip(), tags)
            tag_info = f" with tags: {', '.join(tags)}" if tags else ""
            return f"Note successfully added! (ID: {result.id}){tag_info}"
        except Exception as e:
            return f"Error adding note: {str(e)}"
    
    def edit_note(self, note_id, new_text=None, new_tags=None):
        try:
            result = self.service.edit_note(note_id, new_text, new_tags)
            return f"Note (ID: {note_id}) successfully updated!"
        except Exception as e:
            return f"Error editing note: {str(e)}"
    
    def delete_note(self, note_id):
        try:
            self.service.delete_note(note_id)
            return f"Note (ID: {note_id}) successfully deleted!"
        except Exception as e:
            return f"Error deleting note: {str(e)}"
    
    def search_notes(self, query):
        try:
            results = self.service.search_notes(query)
            if not results:
                return f"No notes found for query '{query}'"
            
            output = ["Note search results:"]
            for note in results:
                truncated_text = self._truncate_text(note.text, self.SEARCH_RESULT_TRUNCATE)
                note_info = f"{truncated_text}"
                if note.tags:
                    note_info += f" | Tags: {', '.join(note.tags)}"
                note_info += f" | ID: {note.id}"
                output.append(note_info)
            
            return "\n".join(output)
        except Exception as e:
            return f"Error searching notes: {str(e)}"
    
    def search_notes_by_tag(self, tag):
        try:
            results = self.service.search_by_tag(tag)
            if not results:
                return f"No notes found with tag '{tag}'"
            
            output = [f"Notes with tag '{tag}':"]
            for note in results:
                truncated_text = self._truncate_text(note.text, self.SEARCH_RESULT_TRUNCATE)
                note_info = f"{truncated_text}"
                if note.tags:
                    note_info += f" | Tags: {', '.join(note.tags)}"
                note_info += f" | ID: {note.id}"
                output.append(note_info)
            
            return "\n".join(output)
        except Exception as e:
            return f"Error searching by tag: {str(e)}"
    
    def list_notes(self):
        try:
            notes = self.service.get_all_notes()
            if not notes:
                return "Note list is empty"
            
            output = ["All notes:"]
            for note in notes:
                truncated_text = self._truncate_text(note.text, self.LIST_RESULT_TRUNCATE)
                note_info = f"{truncated_text}"
                if note.tags:
                    note_info += f" | Tags: {', '.join(note.tags)}"
                note_info += f" | ID: {note.id}"
                output.append(note_info)
            
            return "\n".join(output)
        except Exception as e:
            return f"Error getting note list: {str(e)}"
    
    def _truncate_text(self, text, max_length):
        if len(text) <= max_length:
            return text
        return text[:max_length] + '....'
