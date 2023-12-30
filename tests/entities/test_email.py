import pytest
from core.entities import Email

@pytest.fixture
def email():
    return Email("john.doe@example.com", 1)

def test_init(email):
    assert email.email == "john.doe@example.com"
    assert email.person_id == 1
    
def test_add_email_to_session(mock_session, email):
    mock_session.add.assert_not_called()
    mock_session.add(email)
    mock_session.add.assert_called_once_with(email)