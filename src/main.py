"""
CLI entry point for the personal assistant.

Provides a simple command loop that delegates actions to command classes.
"""

from src.commands import ContactsCommand, NotesCommand, BirthdaysCommand, SearchCommand


def main():
    contacts_cmd = ContactsCommand()
    notes_cmd = NotesCommand()
    birthdays_cmd = BirthdaysCommand()
    search_cmd = SearchCommand()

    print(
        "Personal Assistant CLI. Type 'help' to see available commands. Type 'exit' to quit."
    )

    while True:
        raw = input("> ").strip()
        if not raw:
            continue

        if raw.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if raw.lower() == "help":
            print(
                "Available commands:\n"
                "  add-contact <name> [phone] [email] [address] [birthday]\n"
                "  list-contacts\n"
                "  search-contacts <query>\n"
                "  add-note <text> [#tag1 #tag2 ...]\n"
                "  list-notes\n"
                "  search-notes <query>\n"
                "  search-notes-tag <tag>\n"
                "  birthdays <days>\n"
                "  search <query>   (global search)\n"
                "  help\n"
                "  exit"
            )
            continue

        parts = raw.split()
        command = parts[0].lower()
        args = parts[1:]

        try:
            if command == "add-contact":
                if not args:
                    print(
                        "Usage: add-contact <name> [phone] [email] [address] [birthday]"
                    )
                    continue
                name = args[0]
                phone = args[1] if len(args) > 1 else None
                email = args[2] if len(args) > 2 else None
                address = args[3] if len(args) > 3 else None
                birthday = args[4] if len(args) > 4 else None
                print(contacts_cmd.add_contact(name, phone, email, address, birthday))

            elif command == "list-contacts":
                print(contacts_cmd.list_contacts())

            elif command == "search-contacts":
                if not args:
                    print("Usage: search-contacts <query>")
                    continue
                print(contacts_cmd.search_contacts(" ".join(args)))

            elif command == "add-note":
                if not args:
                    print("Usage: add-note <text> [#tag1 #tag2 ...]")
                    continue
                # tags start with '#'
                text_parts = [a for a in args if not a.startswith("#")]
                tag_parts = [a[1:] for a in args if a.startswith("#")]
                text = " ".join(text_parts)
                print(notes_cmd.add_note(text, tags=tag_parts or None))

            elif command == "list-notes":
                print(notes_cmd.list_notes())

            elif command == "search-notes":
                if not args:
                    print("Usage: search-notes <query>")
                    continue
                print(notes_cmd.search_notes(" ".join(args)))

            elif command == "search-notes-tag":
                if not args:
                    print("Usage: search-notes-tag <tag>")
                    continue
                print(notes_cmd.search_notes_by_tag(args[0]))

            elif command == "birthdays":
                if not args:
                    print("Usage: birthdays <days>")
                    continue
                print(birthdays_cmd.upcoming(args[0]))

            elif command == "search":
                if not args:
                    print("Usage: search <query>")
                    continue
                print(search_cmd.global_search(" ".join(args)))

            else:
                print("Unknown command. Type 'help' to see available commands.")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
