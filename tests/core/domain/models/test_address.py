import pytest
from src.core.domain.models.address import Address

def test_address_creation():
    address = Address(id=1, address_line_1='line1', address_line_2='line2', city='city', state='state', zip_code='zip', person_id=1)
    assert address.id == 1
    assert address.address_line_1 == 'line1'
    assert address.address_line_2 == 'line2'
    assert address.city == 'city'
    assert address.state == 'state'
    assert address.zip_code == 'zip'
    assert address.person_id == 1