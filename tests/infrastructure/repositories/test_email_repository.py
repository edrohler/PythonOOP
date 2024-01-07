import pytest
from src.infrastructure.repositories.generic_repository import GenericRepository
from src.infrastructure.orm.entities.email import Email

@pytest.fixture
def email_repository(test_session, mock_logger):
    return GenericRepository(test_session, Email, mock_logger)

def test_add_and_retrieve_email(email_repository, test_session):
    new_email = Email(email_address="test1@nomail.com", person_id=1)
    email_repository.add(new_email)
    test_session.commit()
    
    retrieved_email = email_repository.get_by_id(new_email.id)
    assert retrieved_email is not None
    assert retrieved_email.email_address == "test1@nomail.com"
    
def test_update_email(email_repository, test_session):
    email = Email(email_address="test1@nomail.com")
    email_repository.add(email)
    test_session.commit()
    
    retrieved_email = email_repository.get_by_id(email.id)
    retrieved_email.email_address = "test2@nomail.com"
    email_repository.update(retrieved_email)
    test_session.commit()
    
    updated_email = email_repository.get_by_id(email.id)
    assert updated_email is not None
    assert updated_email.email_address == "test2@nomail.com"
    
def test_delete_email(email_repository, test_session):
    email_to_delete = Email(email_address="test1@nomail.com")
    email_repository.add(email_to_delete)
    test_session.commit()
    
    email_repository.delete(email_to_delete)
    test_session.commit()
    
    deleted_email = email_repository.get_by_id(email_to_delete.id)
    assert deleted_email is None
    
    
    