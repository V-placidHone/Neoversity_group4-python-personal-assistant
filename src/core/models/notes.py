# Defines the Note class:
#  - attributes: text, list of tags
#  - helper methods: __str__(), to_dict(), from_dict()

from typing import List, Optional
from uuid import UUID, uuid4


class Text:
    """Represents the text content of a note with validation."""

    def __init__(self, content: str):
        if not isinstance(content, str):
            raise ValueError("Text must be a string")
        if not content.strip():
            raise ValueError("Text cannot be empty")
        self.content: str = content.strip()

    def __str__(self):
        return self.content

    # Make Text behave like a string for common operations used in commands
    def __len__(self) -> int:
        return len(self.content)

    def __getitem__(self, key):
        return self.content[key]

    def lower(self) -> str:
        return self.content.lower()


class Tag:
    """Represents a single tag with validation."""

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise ValueError("Tag name must be a string")
        self.name: str = name.strip()

    def __str__(self):
        return self.name

    def lower(self) -> str:
        return self.name.lower()


class Note:
    def __init__(
        self,
        text: Text,
        tags: Optional[List[Tag]] = None,
        note_id: Optional[UUID] = None,
    ):
        """
        Initialize a note.
        :param note_id: unique identifier (UUID, optional)
        :param text: Text object containing note text
        :param tags: list of Tag objects (optional)
        """
        self.id: UUID = note_id or uuid4()
        self.text: Text = text
        self.tags: List[Tag] = tags or []

    def to_dict(self) -> dict:
        """Returns a dictionary for saving to a file or JSON."""
        return {
            "id": str(self.id),
            "text": str(self.text),
            "tags": [str(tag) for tag in self.tags],
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Note from a dictionary."""
        text = Text(data.get("text", ""))
        tags = [Tag(name) for name in data.get("tags", [])]
        note_id = UUID(data["id"]) if "id" in data else None
        return cls(text=text, tags=tags, note_id=note_id)

    def __str__(self):
        """Nicely formatted note display for CLI."""
        tags_str = ", ".join(str(tag) for tag in self.tags) if self.tags else "No tags"
        return f"Note[{self.id}]: {self.text} | Tags: {tags_str}"
