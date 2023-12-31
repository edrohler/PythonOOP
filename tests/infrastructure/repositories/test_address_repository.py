import pytest
from src.infrastructure.repositories.generic_repository import GenericRepository
from src.infrastructure.orm.entities.address import Address

@pytest.fixture
def address_repository(test_session):
    return GenericRepository(test_session, Address)

def test_add_and_retrieve_address(address_repository, test_session):
    new_address = Address(address_line_1="123 Main St", city="Anytown", state="NY", zipcode="12345", person_id=1)
    address_repository.add(new_address)
    test_session.commit()

    retrieved_address = address_repository.get_by_id(new_address.id)
    assert retrieved_address is not None
    assert retrieved_address.address_line_1 == "123 Main St"
    assert retrieved_address.city == "Anytown"
    assert retrieved_address.state == "NY"
    assert retrieved_address.zipcode == "12345"