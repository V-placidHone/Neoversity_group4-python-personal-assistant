# Provides birthday-related logic:
#  - find upcoming birthdays within N days


class BirthdayService:
    def __init__(self, store):
        self.store = store  # expects .load() and .save()
