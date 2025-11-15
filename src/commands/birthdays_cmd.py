

#create  class with method upcoming_birthdays that returns contacts with upcoming birthdays within N  ///renamed to BirrthdayService

#reuse helper from dates.py             /// Not sure which one you mean
# src/commands/birthdays_cmd.py

from services.birthday_service import BirthdayService

from some_store_module import Store  # як у вашому проєкті

class BirthdaysCommand:
    def __init__(self, store: Store):
        self.service = BirthdayService(store)

    def upcoming(self, days_ahead: int = 7):
        result = self.service.print_upcoming_birthdays(days_ahead)
        print(result)
