import pytest
from src.core.domain.models.person import Person
from src.core.serialization.person import PersonApiSchema

@pytest.fixture
def person_api_schema():
    return PersonApiSchema()

def test_person_api_schema_serialization(person_api_schema):
    person = Person(id=1, first_name="first_name", last_name="last_name", gender="A", age=34)
    serialized_data = person_api_schema.dump(person)
    assert serialized_data["id"] == 1
    assert serialized_data["first_name"] == "first_name"
    assert serialized_data["last_name"] == "last_name"
    assert serialized_data["gender"] == "A"
    assert serialized_data["age"] == 34
    
def test_person_api_schema_deserialization(person_api_schema):
    data = {"id": 1, "first_name": "first_name", "last_name": "last_name", "gender": "A", "age": 34 }
    person = person_api_schema.load(data)
    assert person.id == 1
    assert person.first_name == "first_name"
    assert person.last_name == "last_name"
    assert person.gender == "A"
    assert person.age == 34