from datetime import datetime
from .fields import Name, Phone, Birthday, Email, Address

class Record:
    def __init__(self, name):
        self.name = Name(name)

    def add_phone(self, phone):

    def remove_phone(self, phone):

    def edit_phone(self, old_phone, new_phone):
        
    def find_phone(self, phone):

    def add_birthday(self, birthday):

    def add_email(self, email):

    def add_address(self, address):
        
    def __str__(self):