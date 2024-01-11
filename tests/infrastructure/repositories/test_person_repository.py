from datetime import datetime
from pytest_mock import mocker
from sqlalchemy.exc import IntegrityError
import pytest
from src.infrastructure.repositories.generic_repository import GenericRepository
from src.infrastructure.orm.entities.person import Person

@pytest.fixture
def person_repository(test_session, mock_logger):
    # Create a Person repository for testing
    return GenericRepository(test_session, Person, mock_logger)

@pytest.fixture
def test_people(test_session, mock_logger):
    # Create a Person repository for testing
    person_repository = GenericRepository(test_session, Person, mock_logger)
    person_repository.add(Person(first_name="John", last_name="Doe"))
    person_repository.add(Person(first_name="Jane", last_name="Doe"))
    person_repository.add(Person(first_name="Alice", last_name="Smith"))
    person_repository.add(Person(first_name="Bob", last_name="Smith"))
    test_session.commit()
    return person_repository
    
def test_get_all_people(test_people):
    people = test_people.get_all()
    assert len(people) == 4

def test_add_and_retrieve_person(person_repository, test_session):
    # Add a person to the test database
    new_person = Person(first_name="John", last_name="Doe")
    person_repository.add(new_person)
    test_session.commit()

    # Retrieve the person and assert the values
    retrieved_person = person_repository.get_by_id(new_person.id)
    assert retrieved_person is not None
    assert retrieved_person.first_name == "John"
    assert retrieved_person.last_name == "Doe"
    assert retrieved_person.created_by == "system"
    assert retrieved_person.created_at is not None
    
def test_update_person(person_repository, test_session):
    # Add a person to the test database
    person = Person(first_name="Alice", last_name="Johnson")
    person_repository.add(person)
    test_session.commit()

    # Retrieve, update, and commit changes
    retrieved_person = person_repository.get_by_id(person.id)
    retrieved_person.last_name = "Smith"  # Change the last_name
    person_repository.update(retrieved_person)
    test_session.commit()

    # Retrieve again and assert the updated values
    updated_person = person_repository.get_by_id(person.id)
    assert updated_person is not None
    assert updated_person.first_name == "Alice"
    assert updated_person.last_name == "Smith"
    assert updated_person.created_by == "system"
    assert updated_person.created_at is not None
    assert updated_person.updated_by == "system"
    assert updated_person.updated_at is not None
    
def test_update_nonexistent_person(person_repository):
    # Create a Person object without adding it to the database
    nonexistent_person = Person(first_name="Nonexistent", last_name="Person")

    # Attempt to update the nonexistent person should raise an exception
    with pytest.raises(ValueError):
        person_repository.update(nonexistent_person)
    

def test_delete_person(person_repository, test_session):
    person_to_delete = Person(first_name="Mike", last_name="Smith", created_by="test", created_at=datetime.utcnow())
    person_repository.add(person_to_delete)
    test_session.commit()

    person_repository.delete(person_to_delete)
    test_session.commit()

    deleted_person = person_repository.get_by_id(person_to_delete.id)
    assert deleted_person is None
    
def test_delete_nonexistent_person(person_repository):
    # Create a Person object without adding it to the database
    nonexistent_person = Person(first_name="Nonexistent", last_name="Person")

    # Attempt to delete the nonexistent person should raise an exception
    with pytest.raises(ValueError):
        person_repository.delete(nonexistent_person)

def test_add_duplicate_person(person_repository):
    person = Person(first_name="Jane", last_name="Doe")
    person_repository.add(person)

    duplicate_person = Person(first_name="Jane", last_name="Doe")
    with pytest.raises(IntegrityError):
        person_repository.add(duplicate_person)
    
def test_add_person_with_null_first_name(person_repository):
    person = Person(first_name=None, last_name="Doe")
    
    with pytest.raises(IntegrityError):
        person_repository.add(person)
    
def test_add_person_with_null_last_name(person_repository):
    person = Person(first_name="Jane", last_name=None)
    
    with pytest.raises(IntegrityError):
        person_repository.add(person)
