import pickle
from utils.table_response import TableResponse
from dataclasses import dataclass
from pathlib import Path
from .note import Note

@dataclass
class NoteManager:
    pickle_file = 'note_book.pickle'
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        self.notes = []
        if self.file_path.exists():
            self.load_from_file()
            
    def save_to_file(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self.notes, file)

    def load_from_file(self):
        try:
            with open(self.file_path, "rb") as file:
                self.notes = pickle.load(file)
        except FileNotFoundError:
            self.notes = []

    def add_note(self, note: Note):
        self.notes.append(note)

    def search_notes(self, query:str) -> Note:
        for note in self.notes:
            if note.title == query:
                return note
        return None

    def delete_note(self, title:str) -> Note:
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                return note
        return None

    def edit_note(self, title:str, new_content:str) -> Note:
        note = self.search_notes(title)
        if note:
            note.change(new_content)
        return note
    
    def list_notes(self) -> list[Note]:
        return self.notes
    
    def __repr__(self):
        body = [[note.title, note.value, ', '.join(note.tags)] for note in self.notes] if self.notes else [
            ["", "", ""]]
        return repr(TableResponse(headers=["Title", "Content", "Tags"], body=body))