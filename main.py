from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from pathlib import Path
from colorama import Fore
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
    PHONE_DELIMITER
)
from utils.decorators import input_error
from datetime import datetime
from utils.table_response import TableResponse

class PersonalAssistant:
    def __init__(self):
        self.address_book = AddressBook(CONTACTS_FILE)
        self.note_manager = NoteManager(NOTES_FILE)
        
        self.commands = {
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
            "help": self.show_help,
            "add-tag": self.add_tag,
            "remove-tag": self.remove_tag,
            "change-tag": self.change_tag,
            "get-tag": self.get_tag,
            "sort-tag": self.sort_tag
        }
        
        self.command_completer = WordCompleter(
            list(self.commands.keys()) + ["close", "exit", "goodbye", "quit"],
            ignore_case=True
        )
        
        self.session = PromptSession(
            completer=self.command_completer,
            complete_while_typing=True
        )

    @input_error
    def add_tag(self, args: list):
        if len(args) < 2:
            raise ValueError("Please provide note title and at least one tag.")
        
        note_title = args[0]
        tag = " ".join(args[1:])
        notes = self.note_manager.search_notes(note_title)

        if isinstance(notes, list):
            for note in notes:
                note.add_tag(tag)
                self.note_manager.save_to_file()  
            return f"Tag '{tag}' added to {len(notes)} note(s) with title '{note_title}' successfully."
        else:
            notes.add_tag(tag)  
            self.note_manager.save_to_file()  
            return f"Tag '{tag}' added to note '{note_title}' successfully."
        
    @input_error
    def change_tag(self, args: list):
        if len(args) != 3:
            raise ValueError("Please provide note title, old tag and new tag.")
        
        note_title, old_tag, new_tag = args[0], args[1], args[2]
        notes = self.note_manager.search_notes(note_title)
        
        if not notes:
            raise KeyError(f"Note '{note_title}' not found.")
    
        if isinstance(notes, list):
            updated_count = 0
            for note in notes:
                if old_tag in note.tags:
                    note.remove_tag(old_tag)
                    note.add_tag(new_tag)
                    updated_count += 1
            if updated_count > 1:
                self.note_manager.save_to_file()  
                return f"Tag '{old_tag}' changed to '{new_tag}' for {updated_count} note(s) with title '{note_title}' successfully."
            else:
                raise ValueError(f"Tag '{old_tag}' not found in any note with title '{note_title}'.")
        else:
            if old_tag in notes.tags:
                notes.remove_tag(old_tag)
                notes.add_tag(new_tag)
                self.note_manager.save_to_file()  
                return f"Tag '{old_tag}' changed to '{new_tag}' for note '{note_title}' successfully."
            else:
                raise ValueError(f"Tag '{old_tag}' not found in note '{note_title}'.")
        
    
    @input_error
    def remove_tag(self, args: list):
        if len(args) != 2:
            raise ValueError("Please provide note title and tag which you want to remove.")
        
        note_title, tag = args[0], args[1]
        notes = self.note_manager.search_notes(note_title)

        if isinstance(notes, list):
            removed_count = 0
            for note in notes:
                if note.remove_tag(tag):
                    removed_count += 1
            if removed_count > 1:
                self.note_manager.save_to_file()  
                return f"Tag '{tag}' removed from {removed_count} note(s) with title '{note_title}' successfully."
            else:
                raise ValueError(f"Tag '{tag}' not found in any note with title '{note_title}'.")
        else:
            if notes.remove_tag(tag):
                self.note_manager.save_to_file()  
                return f"Tag '{tag}' removed from note '{note_title}' successfully."
            else:
                raise ValueError(f"Tag '{tag}' not found in note '{note_title}'.")
        
    @input_error
    def get_tag(self, args: list):
        if not args:
            raise ValueError("Please provide exactly one tag.")
        
        tag = ' '.join(args)
        matching_notes = []
        for note in self.note_manager.list_notes():
            if tag in note.tags:
                matching_notes.append(note)
        
        if matching_notes:
            headers = ["Title", "Content", "Tags"]
            body = [[note.title, note.value, ', '.join(note.tags)] for note in matching_notes]
            table = TableResponse(headers, body)
            return repr(table)
        else:
            raise ValueError(f"No notes found with tag '{tag}'.")
        
    @input_error
    def sort_tag(self, args: list):
        if not args:
            raise ValueError("Please provide exactly one tag.")
        
        tag = ' '.join(args)
        matching_notes = []
        for note in self.note_manager.list_notes():
            if tag in note.tags:
                matching_notes.append(note)
        
        if matching_notes:
            headers = ["Title", "Content", "Tags"]
            body = [[note.title, note.value, ', '.join(note.tags)] for note in matching_notes]
            table = TableResponse(headers, body)
            return repr(table)
        else:
            raise ValueError(f"No notes found with tag '{tag}'.")

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
        if len(args) < 2:
            raise ValueError("Please provide both a name and at least one contact detail (e.g., phone number, email, etc.).")
    
        name = args[0]

        contact_details = args[1:]  

        record = self.address_book.find(name)
        updated_details = []

        for detail in contact_details:
            updated = False
            if "@" in detail:  
                record.add_email(detail)
                updated = True
            elif Phone.validate(detail):
                record.add_phone(detail)
                updated = True
            elif len(detail.split(PHONE_DELIMITER)) == 2:
                old, new = detail.split(PHONE_DELIMITER)
                if Phone.validate(old) and Phone.validate(new):
                    record.edit_phone(old, new)
                    updated = True
            else:
                try:
                    datetime.strptime(detail, "%d.%m.%Y")
                    record.add_birthday(detail)
                    updated = True
                except ValueError:
                    record.add_address(detail)
                    updated = True
            
            if updated:
                updated_details.append(detail)

        self.address_book.save_to_file()  

        return f"Contact '{name}' was {'' if updated_details else 'not '}updated. Details: [{', '.join(updated_details)}]." 

    @input_error
    def delete_contact(self, args):
        if len(args) != 1:
            raise ValueError("Give me exactly one name please.")
        
        name = args[0]
        record = self.address_book.delete(name)

        if record:
            self.address_book.save_to_file()
            return f"Contact {name} deleted."
        
        raise KeyError()
    
    @input_error
    def search_contact(self, args):
        if len(args) != 1 or len(args[0]) < 3:
            raise ValueError("Query must contains 1 item with at least 3 symbols")
        
        query = args[0]

        result = dict()
        self.address_book.find_by_name(query, result)
        self.address_book.find_by_phone(query, result)
        self.address_book.find_by_email(query, result)
        self.address_book.find_by_address(query, result)

        result_string = "\n".join(str(record) for record in result.values())

        return result_string.casefold().replace(query.casefold(), self.colorize_text(query.casefold()))
        

    def colorize_text(self, text):
        return Fore.GREEN + text + Fore.RESET
    

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
        if len(args) != 1:
            raise ValueError("Please provide exactly one contact name.")
    
        name = args[0]
        record = self.address_book.find(name)
    
        if not record:
            return f"Contact '{name}' not found."
    
        birthday = record.birthday
        if not birthday:
            return f"No birthday set for '{name}'."
    
        return f"Birthday for '{name}' is on {birthday}."
    
    @input_error
    def show_birthdays(self, args):
        days = 7

        if args:
            try:
                days = int(args[0])
            except ValueError:
                return "Please provide a valid number for the period in days."
        
        upcoming_birthdays = self.address_book.get_upcoming_birthdays(days)

        if not upcoming_birthdays:
            return f"No upcoming birthdays within the next {days} days."

        birthdays_str = "\n".join(f"{name}: {birthday}" for name, birthday in upcoming_birthdays.items())
        return f"Upcoming birthdays in the next {days} days:\n{birthdays_str}"

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
        
        while True:
            try:
                user_input = self.session.prompt("Enter a command (or 'help' for help): ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ["close", "exit", "goodbye", "quit"]:
                    print(GOODBYE_MESSAGE)
                    break
                
                command, args = self.parse_input(user_input)
                
                if command in self.commands:
                    result = self.commands[command](args)
                    print(result)
                else:
                    closest_matches = [cmd for cmd in self.commands.keys() 
                                    if cmd.startswith(command[:2]) or 
                                    any(word.startswith(command[:2]) for word in cmd.split('-'))]
                    
                    if closest_matches:
                        print(f"Invalid command. Did you mean one of these? {', '.join(closest_matches)}")
                    else:
                        print("Invalid command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                continue
            except EOFError:
                print(GOODBYE_MESSAGE)
                break

def main():
    assistant = PersonalAssistant()
    assistant.run()

if __name__ == "__main__":
    main()