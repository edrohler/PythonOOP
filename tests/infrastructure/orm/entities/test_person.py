import pytest
from src.infrastructure.orm.entities import Person

@pytest.fixture
def person():
    return Person(first_name="John", last_name="Doe", gender="M", age=30)

def test_person_initialization(person):
    assert person.first_name == "John"
    assert person.last_name == "Doe"
    assert person.gender == "M"
    assert person.age == 30
