from collections import UserDict
from datetime import datetime, timedelta
import pickle
from pathlib import Path

class AddressBook(UserDict):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = Path(file_path)
        if self.file_path.exists():
            self.load_from_file()
            
    def save_to_file(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self):
        try:
            with open(self.file_path, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def add_record(self, record):

    def find(self, name):

    def delete(self, name):

    def find_by_phone(self, phone):

    def find_by_email(self, email):
        
    def find_by_address(self, address_query):

    def get_upcoming_birthdays(self, days=7):