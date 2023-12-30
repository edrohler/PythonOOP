import pytest
from core.entities import Address

@pytest.fixture
def address():
    return Address("123 Main St", "Apt 4B", "New York", "NY", "10001", 1)

def test_init(address):
    assert address.address_line_1 == "123 Main St"
    assert address.address_line_2 == "Apt 4B"
    assert address.city == "New York"
    assert address.state == "NY"
    assert address.zipcode == "10001"
    assert address.person_id == 1
    
def test_add_address_to_session(mock_session, address):
    mock_session.add.assert_not_called()
    mock_session.add(address)
    mock_session.add.assert_called_once_with(address)