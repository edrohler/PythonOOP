import pytest
from src.infrastructure.repositories.generic_repository import GenericRepository
from src.infrastructure.orm.entities.address import Address

@pytest.fixture
def address_repository(test_session, mock_logger):
    return GenericRepository(test_session, Address, mock_logger)

def test_add_and_retrieve_address(address_repository, test_session):
    new_address = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1)
    address_repository.add(new_address)
    test_session.commit()

    retrieved_address = address_repository.get_by_id(new_address.id)
    assert retrieved_address is not None
    assert retrieved_address.address_line_1 == "123 Main St"
    assert retrieved_address.city == "Anytown"
    assert retrieved_address.state == "NY"
    assert retrieved_address.zip_code == "12345"
    
def test_update_address(address_repository, test_session):
    address = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1)
    address_repository.add(address)
    test_session.commit()

    retrieved_address = address_repository.get_by_id(address.id)
    retrieved_address.address_line_1 = "456 Main St"
    address_repository.update()
    test_session.commit()

    updated_address = address_repository.get_by_id(address.id)
    assert updated_address is not None
    assert updated_address.address_line_1 == "456 Main St"
    assert updated_address.city == "Anytown"
    assert updated_address.state == "NY"
    assert updated_address.zip_code == "12345"
    
def test_delete_address(address_repository, test_session):
    address_to_delete = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1)
    address_repository.add(address_to_delete)
    test_session.commit()

    address_repository.delete(address_to_delete)
    test_session.commit()

    deleted_address = address_repository.get_by_id(address_to_delete.id)
    assert deleted_address is None