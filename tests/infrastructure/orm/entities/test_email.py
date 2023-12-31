import pytest
from src.infrastructure.orm.entities import Email

@pytest.fixture
def email():
    return Email(email_address="john.doe@example.com", person_id=1)

def test_email_initialization(email):
    assert email.email_address == "john.doe@example.com"
    assert email.person_id == 1