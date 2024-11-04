from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONTACTS_FILE = DATA_DIR / "contacts.pkl"
NOTES_FILE = DATA_DIR / "notes.pkl"

DATA_DIR.mkdir(exist_ok=True)

WELCOME_MESSAGE = "Welcome to the personal assistant!"
GOODBYE_MESSAGE = "Good bye!"
HELP_MESSAGE = """
Available commands:
Contacts:
    add
    change
    search
    all - Show all contacts
    add-birthday
    show-birthday <name> - Show contact's birthday
    birthdays - Show upcoming birthdays

    Notes:
    note-add <title> <content> [tags] - Add new note
    note-change <title> <new_content> - Edit note
    note-delete <title> - Delete note
    note-find <query> - Search notes

    General:
    help - Show this help
    exit - Exit the program
"""