from dataclasses import dataclass

@dataclass
class Email():
    id: int
    email_address: str
    person_id: int