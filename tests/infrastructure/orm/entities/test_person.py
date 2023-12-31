import pytest
from src.infrastructure.orm.entities import Person

@pytest.fixture
def person():
    return Person(firstname="John", lastname="Doe", gender="M", age=30)

def test_person_initialization(person):
    assert person.firstname == "John"
    assert person.lastname == "Doe"
    assert person.gender == "M"
    assert person.age == 30
