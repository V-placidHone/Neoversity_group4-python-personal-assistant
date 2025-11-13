#переіменуйте як в трелло записана на birhday_service.py

#create  class with method upcoming_birthdays that returns contacts with upcoming birthdays within N  ///renamed to BirrthdayService

#reuse helper from dates.py             /// Not sure which one you mean
from datetime import date

def next_comming_birthdays(birthday, days_ahead):
    today = date.today()
    birthday_list = []
    current_year_birthday = birthday.replace(year=today.year)
    if current_year_birthday < today:
        current_year_birthday = current_year_birthday.replace(year=today.year + 1)
    delta = (current_year_birthday - today).days    
    if 0 <= delta <= days_ahead:
        birthday_list.append(birthday)
    return birthday_list

# Birthday service class suggested solo by helper, I have no idea which one do we need. will love to review your suggestions.
"""
class BirthdayService:
    def __init__(self, contacts):
        self.contacts = contacts

    def upcoming_birthdays(self, days_ahead):
        upcoming = []
        for contact in self.contacts:
            birthday = contact.get('birthday')
            if birthday:
                upcoming.extend(next_comming_birthdays(birthday, days_ahead))
        return upcoming

   
"""