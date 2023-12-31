import pytest
from src.infrastructure.repositories.generic_repository import GenericRepository
from src.infrastructure.orm.entities.email import Email

@pytest.fixture
def email_repository(test_session):
    return GenericRepository(test_session, Email)

def test_add_and_retrieve_email(email_repository, test_session):
    new_email = Email(email_address="test1@nomail.com", person_id=1)
    email_repository.add(new_email)
    test_session.commit()
    
    retrieved_email = email_repository.get_by_id(new_email.id)
    assert retrieved_email is not None
    assert retrieved_email.email_address == "test1@nomail.com"
    
    