from datetime import datetime
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number. Must be 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(phone):
        return bool(re.fullmatch(r'\d{10}', phone))

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(self.value)

class Email(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

    @staticmethod
    def validate(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

class Address(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value)