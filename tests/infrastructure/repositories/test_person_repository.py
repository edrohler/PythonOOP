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
    
def test_update_person(person_repository, test_session):
    # Add a person to the test database
    person = Person(firstname="Alice", lastname="Johnson")
    person_repository.add(person)
    test_session.commit()

    # Retrieve, update, and commit changes
    retrieved_person = person_repository.get_by_id(person.id)
    retrieved_person.lastname = "Smith"  # Change the lastname
    person_repository.update()
    test_session.commit()

    # Retrieve again and assert the updated values
    updated_person = person_repository.get_by_id(person.id)
    assert updated_person is not None
    assert updated_person.firstname == "Alice"
    assert updated_person.lastname == "Smith"
    

def test_delete_person(person_repository, test_session):
    person_to_delete = Person(firstname="Mike", lastname="Smith")
    person_repository.add(person_to_delete)
    test_session.commit()

    person_repository.delete(person_to_delete)
    test_session.commit()

    deleted_person = person_repository.get_by_id(person_to_delete.id)
    assert deleted_person is None

def test_add_duplicate_person(person_repository, test_session):
    person = Person(firstname="Jane", lastname="Doe")
    person_repository.add(person)
    test_session.commit()

    duplicate_person = Person(firstname="Jane", lastname="Doe")
    person_repository.add(duplicate_person)

    with pytest.raises(Exception):
        test_session.commit()
    test_session.rollback()
    
def test_add_person_with_null_firstname(person_repository, test_session):
    person = Person(firstname=None, lastname="Doe")
    person_repository.add(person)

    with pytest.raises(Exception):
        test_session.commit()
    test_session.rollback()
    
def test_add_person_with_null_lastname(person_repository, test_session):
    person = Person(firstname="Jane", lastname=None)
    person_repository.add(person)

    with pytest.raises(Exception):
        test_session.commit()
    test_session.rollback()