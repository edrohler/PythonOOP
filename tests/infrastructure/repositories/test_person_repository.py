import pytest
from src.infrastructure.repositories.generic_repository import GenericRepository
from src.infrastructure.orm.entities.person import Person

@pytest.fixture
def person_repository(test_session):
    # Create a Person repository for testing
    return GenericRepository(test_session, Person)

def test_add_and_retrieve_person(person_repository, test_session):
    # Add a person to the test database
    new_person = Person(firstname="John", lastname="Doe")
    person_repository.add(new_person)
    test_session.commit()

    # Retrieve the person and assert the values
    retrieved_person = person_repository.get_by_id(new_person.id)
    assert retrieved_person is not None
    assert retrieved_person.firstname == "John"
    assert retrieved_person.lastname == "Doe"


