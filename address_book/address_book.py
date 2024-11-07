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
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        return self.data.pop(name, None)

    def find_by_name(self, query, result: dict):
        for key in self.data.keys():
            if query.casefold() in key.casefold():
                result[key] = self.data[key]

    def find_by_phone(self, query, result: dict):
        records = self.data.values()
        for record in records:
            for phone in record.phones:
                if query in phone.value:
                    name = record.name.value
                    if name not in result.keys():
                        result[name] = self.data[name]

    def find_by_email(self, query, result: dict):
        records = self.data.values()
        for record in records:
            if query.casefold() in record.email.value.casefold():
                name = record.name.value
                if name not in result.keys():
                    result[name] = self.data[name]

        
    def find_by_address(self, query, result: dict):
        records = self.data.values()
        for record in records:
            if query.casefold() in record.address.value.casefold():
                name = record.name.value
                if name not in result.keys():
                    result[name] = self.data[name]


    def get_upcoming_birthdays(self, days=7):
        pass
