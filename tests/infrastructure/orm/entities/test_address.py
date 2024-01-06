import pytest
from src.infrastructure.orm.entities import Address

@pytest.fixture
def address():
    return Address(address_line_1="123 Main St", address_line_2="Apt 4B", city="New York", state="NY", zip_code="10001", person_id=1)
    
def test_address_initialization(address):
    assert address.address_line_1 == "123 Main St"
    assert address.address_line_2 == "Apt 4B"
    assert address.city == "New York"
    assert address.state == "NY"
    assert address.zip_code == "10001"
    assert address.person_id == 1