import pytest
from src.core.domain.models.person import Person

def test_person_creation():
    person = Person(id=1, first_name='John', last_name='Doe', gender='Male', age=30)
    assert person.id == 1
    assert person.first_name == 'John'
    assert person.last_name == 'Doe'
    assert person.gender == 'Male'
    assert person.age == 30