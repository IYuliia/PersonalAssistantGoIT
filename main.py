from pathlib import Path
from address_book.address_book import AddressBook
from address_book.record import Record
from address_book.fields import Phone
from notes.note_manager import NoteManager
from utils.constants import (
    CONTACTS_FILE,
    NOTES_FILE,
    WELCOME_MESSAGE,
    GOODBYE_MESSAGE,
    HELP_MESSAGE,
)
from utils.decorators import input_error
from datetime import datetime

class PersonalAssistant:
    def __init__(self):
        self.address_book = AddressBook(CONTACTS_FILE)
        self.note_manager = NoteManager(NOTES_FILE)

    @input_error
    def add_contact(self, args):
            if len(args) < 2:
                raise ValueError("Please provide both a name and at least one contact detail (e.g., phone number, email, etc.).")
    
            name = args[0]
            contact_details = args[1:]  

            record = Record(name)

            for detail in contact_details:
                if "@" in detail:  
                    record.add_email(detail)
                elif Phone.validate(detail):  
                    record.add_phone(detail)
                else:
                    try:
                        datetime.strptime(detail, "%d.%m.%Y")
                        record.add_birthday(detail)
                    except ValueError:
                        record.add_address(detail)

            self.address_book.add_record(record)
            self.address_book.save_to_file()  

            return f"Contact '{name}' added successfully with details: {', '.join(contact_details)}."

    @input_error
    def change_contact(self, args):
    
    @input_error
    def delete_contact(self, args):
        if len(args) != 2:
            raise ValueError("Give me name please.")
        name = args
        record = self.address_book.delete(name)
        if record:
            record.delete(name)
            self.address_book.save_to_file()
            return f"Contact {name} deleted."
        raise KeyError()
    
    @input_error
    def search_contact(self, args):

    @input_error
    def add_birthday(self, args):
        if len(args) < 2:
            raise ValueError("Please provide both a name and a birthday (DD.MM.YYYY).")
        
        name, birthday = args
        record = self.address_book.find(name)
        
        if not record:
            return f"Contact '{name}' not found."
        
        record.add_birthday(birthday)
        self.address_book.save_to_file()
        
        return f"Birthday for '{name}' set to {birthday}."


    @input_error
    def show_birthday(self, args):

    @input_error
    def show_birthdays(self, args):


    @input_error
    def add_note(self, args):
        if len(args) < 2:
            raise ValueError("Give me title and content please.")
        title = args[0]
        content = args[1]
        self.note_manager.add_note(title, content)
        return f"Note '{title}' added successfully."

    @input_error
    def change_note(self, args):
        if len(args) < 2:
            raise ValueError("Give me title and new content please.")
        title = args[0]
        new_content = args[1]
        self.note_manager.edit_note(title, new_content)
        return f"Note '{title}' updated successfully."

    @input_error
    def delete_note(self, args):
        if len(args) != 1:
            raise ValueError("Give me note title please.")
        title = args[0]
        self.note_manager.delete_note(title)
        return f"Note '{title}' deleted successfully."

    @input_error
    def find_notes(self, args):
        if len(args) != 1:
            raise ValueError("Give me search query please.")
        query = args[0]
        notes = self.note_manager.search_notes(query)
        if not notes:
            return "No notes found."
        return "\n\n".join(str(note) for note in notes)

    def show_all_contacts(self, args):
        if not self.address_book:
            return "No contacts available."
        return "\n".join(str(record) for record in self.address_book.values())

    def show_help(self, *args):
        return HELP_MESSAGE

    def parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args

    def run(self):
        print(WELCOME_MESSAGE)
        
        commands = {
            "add": self.add_contact,
            "change": self.change_contact,
            "delete": self.delete_contact,
            "search": self.search_contact,
            "all": self.show_all_contacts,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
            "birthdays": self.show_birthdays,
            "note-add": self.add_note,
            "note-change": self.change_note,
            "note-delete": self.delete_note,
            "note-find": self.find_notes,
            "help": self.show_help
        }
        
        while True:
            user_input = input("Enter a command (or 'help' for help): ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["close", "exit", "goodbye", "quit"]:
                print(GOODBYE_MESSAGE)
                break
            
            command, args = self.parse_input(user_input)
            
            if command in commands:
                result = commands[command](args)
                print(result)
            else:
                print("Invalid command.")

def main():
    assistant = PersonalAssistant()
    assistant.run()

if __name__ == "__main__":
    main()