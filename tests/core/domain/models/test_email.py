from src.core.domain.models.email import Email

def test_email_creation():
    email = Email(id=1, email_address='test@example.com', person_id=1)
    assert email.id == 1
    assert email.email_address == 'test@example.com'
    assert email.person_id == 1