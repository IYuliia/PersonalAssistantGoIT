import pickle
from pathlib import Path
from .note import Note

class NoteManager:
    def __init__(self, file_path):
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

    def add_note(self, title, content, tags=None):

    def search_notes(self, query):

    def delete_note(self, title):

    def edit_note(self, title, new_content):