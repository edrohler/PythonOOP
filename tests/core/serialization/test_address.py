import pytest
from src.core.domain.models.address import Address
from src.core.serialization.address import AddressApiSchema


@pytest.fixture
def address_api_schema():
    return AddressApiSchema()

def test_address_api_schema_serialization(address_api_schema):
    address = Address(id=1, address_line_1='line1', address_line_2='line2', city='city', state='state', zip_code='zip', person_id=1)
    serialized_data = address_api_schema.dump(address)
    assert serialized_data['id'] == 1
    assert serialized_data['address_line_1'] == 'line1'
    assert serialized_data['address_line_2'] == 'line2'
    assert serialized_data['city'] == 'city'
    assert serialized_data['state'] == 'state'
    assert serialized_data['zip_code'] == 'zip'
    assert serialized_data['person_id'] == 1

def test_address_api_schema_deserialization(address_api_schema):
    data = {'id': 1, 'address_line_1': 'line1', 'address_line_2': 'line2', 'city': 'city', 'state': 'state', 'zip_code': 'zip', 'person_id': 1}
    address = address_api_schema.load(data)
    assert address.id == 1
    assert address.address_line_1 == 'line1'
    assert address.address_line_2 == 'line2'
    assert address.city == 'city'
    assert address.state == 'state'
    assert address.zip_code == 'zip'
    assert address.person_id == 1