from dataclasses import dataclass


@dataclass
class Address():
    street: str
    city: str
    state: str
    zip_code: str
    person_id: int