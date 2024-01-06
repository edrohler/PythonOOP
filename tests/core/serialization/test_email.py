import pytest
from src.core.domain.models.email import Email
from src.core.serialization.email import EmailApiSchema

@pytest.fixture
def email_api_schema():
    return EmailApiSchema()

def test_email_api_schema_serialization(email_api_schema):
    email = Email(id=1, email_address='email', person_id=1)
    serialized_data = email_api_schema.dump(email)
    assert serialized_data['id'] == 1
    assert serialized_data['email_address'] == 'email'
    assert serialized_data['person_id'] == 1
    
def test_email_api_schema_deserialization(email_api_schema):
    data = {'id': 1, 'email_address': 'email', 'person_id': 1}
    email = email_api_schema.load(data)
    assert email.id == 1
    assert email.email_address == 'email'
    assert email.person_id == 1