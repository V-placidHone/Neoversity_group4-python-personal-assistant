# Entry point of the application.
# Runs the CLI loop (via input()) and dispatches commands.
# Interacts with services (Contacts, Notes, Birthdays, Search).
# services/notes_service.py

from core.models.notes import Note
from services.notes_service import NotesService

def main():
    service = NotesService()

    # Додаємо нотатки
    service.add(Note(1, "Перша нотатка", ["важливе", "робота"]))
    service.add(Note(2, "Друга нотатка", ["робота"]))
    service.add(Note(3, "Тестова нотатка", ["тест"]))

    # Виводимо всі нотатки
    print("Всі нотатки після додавання:")
    for note in service.get_all():
        print(note)

    # Пошук за тегами
    print("\nNotes з тегом 'робота':", service.find_by_tags(tags=["робота"]))

    # Пошук за текстом
    print("Notes з текстом 'тест':", service.find_by_tags(text="тест"))

    # Оновлення нотатки
    service.update(1, text="Оновлена перша нотатка", tags=["важливе", "терміново"])
    print("\nПісля оновлення нотатки 1:")
    for note in service.get_all():
        print(note)

    # Видалення нотатки
    service.delete(2)
    print("\nПісля видалення нотатки 2:")
    for note in service.get_all():
        print(note)

if __name__ == "__main__":
    main()


   
     

