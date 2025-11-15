# src/core/utils/dates.py


from datetime import date

 # Функція для перевірки, чи наближається день народження 
def is_birthday_coming(birthday: date, days_ahead: int = 7) -> bool:
    today = date.today()

    # 1. ДН у поточному році
    try:
        birthday_this_year = birthday.replace(year=today.year)
    except ValueError:
        # якщо 29.02 в невисокосний рік → робимо 28.02
        birthday_this_year = date(today.year, 2, 28)

    # 2. Якщо вже минув ⇒ переносимо на наступний рік
    if birthday_this_year < today:
        try:
            birthday_this_year = birthday.replace(year=today.year + 1)
        except ValueError:
            birthday_this_year = date(today.year + 1, 2, 28)

   
    ver_birthday_soon = (birthday_this_year - today).days 
    
    return 0 <=  ver_birthday_soon <= days_ahead  # returns True if birthday is within days_ahead; 


