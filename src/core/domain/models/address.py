from dataclasses import dataclass


@dataclass
class Address():
    id: int
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: str
    person_id: int