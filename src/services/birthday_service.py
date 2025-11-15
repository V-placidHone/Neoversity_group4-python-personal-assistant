# Provides birthday-related logic:
#  - find upcoming birthdays within N days
from typing import Any

# src/services/birthday_service.py
class BirthdayService:
    def __init__(self, store):
        # store — об’єкт, який має методи load() і save()
        self.store = store

    def add_birthday(self, name: str, birthday: date) -> None:
        contacts = self.store.load()
        contacts.append({
            "name": name,
            "birthday": birthday,
        })
        self.store.save(contacts)

    def update_birthday(self, name: str, new_birthday: date) -> None:
        contacts = self.store.load()
        for contact in contacts:
            if contact.get("name") == name:
                contact["birthday"] = new_birthday
                break
        self.store.save(contacts)

    def get_upcoming_birthdays(self, days_ahead: int = 7):
        contacts = self.store.load()
        upcoming = []

        for contact in contacts:
            birthday = contact.get("birthday")
            if birthday and is_birthday_coming(birthday, days_ahead):
                upcoming.append(contact)

        return upcoming

    def print_upcoming_birthdays(self, days_ahead: int = 7) -> str:
        upcoming = self.get_upcoming_birthdays(days_ahead)

        if not upcoming:
            return f"No contacts found with birthdays within next {days_ahead} days"

        lines = [f"Contacts with birthdays within next {days_ahead} days:"]
        for contact in upcoming:
            lines.append(f"- {contact.get('name')}: {contact.get('birthday')}")

        return "\n".join(lines)
