from datetime import datetime
from .fields import Name, Phone, Birthday, Email, Address

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):

    def edit_phone(self, old_phone, new_phone):
        
    def find_phone(self, phone):

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)
        
    def __str__(self):
        phone_str = "; ".join(p.value for p in self.phones) if self.phones else "No phone numbers"
        birthday_str = f"Birthday: {self.birthday.value}" if self.birthday else "No birthday set"
        email_str = f"Email: {self.email.value}" if self.email else "No email set"
        address_str = f"Address: {self.address.value}" if self.address else "No address set"
    
        details = [f"Name: {self.name.value}", f"Phones: {phone_str}", birthday_str, email_str, address_str]
        return "\n".join(details)