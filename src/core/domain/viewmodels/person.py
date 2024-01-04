from src.core.domain.viewmodels import email
from src.core.domain.viewmodels import address


class Person:
    firstname: str
    lastname: str
    gender: str
    addresses: address = []
    emails: email = []