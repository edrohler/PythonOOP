from src.core.domain.viewmodels import email
from src.core.domain.viewmodels import address


class Person:
    def __init__(self, first_name: str, last_name: str, gender: str, addresses: address = None, emails: email = None):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.addresses = addresses
        self.emails = emails