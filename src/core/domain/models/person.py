from dataclasses import dataclass
from src.core.domain.models import email
from src.core.domain.models import address

@dataclass
class Person():
    id: int
    first_name: str
    last_name: str
    gender: str
    age: int