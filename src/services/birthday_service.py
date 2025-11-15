# Provides birthday-related logic:
#  - find upcoming birthdays within N days
from typing import Any


class BirthdayService:
    def __init__(self, store: Any | None = None) -> None:
        self.store = store
