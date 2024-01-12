from datetime import datetime, timedelta
import pytest
from src.infrastructure.repositories.generic_repository import GenericRepository
from src.infrastructure.orm.entities.email import Email

@pytest.fixture
def email_repository(test_session, mock_logger):
    return GenericRepository(test_session, Email, mock_logger)

@pytest.fixture
def test_emails(test_session, mock_logger):
    email_repository = GenericRepository(test_session, Email, mock_logger)
    email_repository.add(Email(email_address="naomail1@nomail.com", person_id=1))
    email_repository.add(Email(email_address="naomail2@nomail.com", person_id=1))
    email_repository.add(Email(email_address="naomail3@nomail.com", person_id=1))
    email_repository.add(Email(email_address="naomail4@nomail.com", person_id=1))
    return email_repository

def test_get_all_emails(test_emails):
    emails = test_emails.get_all()
    assert len(emails) == 4
    

def test_add_and_retrieve_email(email_repository, test_session):
    new_email = Email(email_address="test1@nomail.com", person_id=1, created_by="test")
    email_repository.add(new_email)
    test_session.commit()
    
    retrieved_email = email_repository.get_by_id(new_email.id)
    assert retrieved_email is not None
    assert retrieved_email.email_address == "test1@nomail.com"
    assert retrieved_email.person_id == 1
    assert retrieved_email.created_by == "system"
    assert retrieved_email.created_at is not None
    
def test_update_email(email_repository, test_session):
    email = Email(email_address="test1@nomail.com", person_id=1)
    email_repository.add(email)
    test_session.commit()
    
    retrieved_email = email_repository.get_by_id(email.id)
    retrieved_email.email_address = "test2@nomail.com"
    email_repository.update(retrieved_email)
    test_session.commit()
    
    updated_email = email_repository.get_by_id(email.id)
    assert updated_email is not None
    assert updated_email.email_address == "test2@nomail.com"
    assert updated_email.person_id == 1
    assert updated_email.created_by == "system"
    assert updated_email.created_at is not None
    assert updated_email.updated_by == "system"
    assert updated_email.updated_at is not None
    
def test_update_email_with_nonexistent_email(email_repository):
    email = Email(email_address="nomail@nomail.com", person_id=1)
    with pytest.raises(ValueError):
        email_repository.update(email)
        
def test_update_email_raises_exception(email_repository, mocker):
    email = Email(email_address="mail@nomail.com", person_id=1)
    email_repository.add(email)
    mocker.patch.object(GenericRepository, "update", side_effect=Exception("Test exception"))
    with pytest.raises(Exception):
        email_repository.update(email)
        
def test_delete_email(email_repository, test_session):
    email_to_delete = Email(email_address="test1@nomail.com", person_id=1, created_by="test", created_at=datetime.utcnow())
    email_repository.add(email_to_delete)
    test_session.commit()
    
    email_repository.delete(email_to_delete)
    test_session.commit()
    
    deleted_email = email_repository.get_by_id(email_to_delete.id)
    assert deleted_email is None
    
def test_delete_email_with_nonexistent_email(email_repository):
    email = Email(email_address="nomail@nomail", person_id=1, created_by="test", created_at=datetime.utcnow())
    with pytest.raises(ValueError):
        email_repository.delete(email)    
    
def test_delete_email_raises_exception(email_repository, mocker):
    email_to_delete = Email(email_address="mail@nomail.com", person_id=1, created_by="test", created_at=datetime.utcnow())
    email_repository.add(email_to_delete)
    mocker.patch.object(GenericRepository, "delete", side_effect=Exception("Test exception"))

    with pytest.raises(Exception):
        email_repository.delete(email_to_delete)