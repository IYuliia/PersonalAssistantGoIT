import re
from datetime import datetime
from address_book.fields import Email, Phone

DATE_REGEX = r'\d{2}\.\d{2}\.\d{4}' 

def is_date(detail):
    try:
        datetime.strptime(detail, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def is_address(detail):
    return not (Email.validate(detail) or Phone.validate(detail) or is_date(detail))