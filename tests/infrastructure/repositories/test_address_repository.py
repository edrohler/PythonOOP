from datetime import datetime, timedelta
import pytest
from src.infrastructure.repositories.generic_repository import GenericRepository
from src.infrastructure.orm.entities.address import Address

@pytest.fixture
def address_repository(test_session, mock_logger):
    return GenericRepository(test_session, Address, mock_logger)

@pytest.fixture
def test_addresses(test_session, mock_logger):
    address_repository = GenericRepository(test_session, Address, mock_logger)
    address_repository.add(Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1))
    address_repository.add(Address(address_line_1="456 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1))
    address_repository.add(Address(address_line_1="789 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1))
    address_repository.add(Address(address_line_1="101112 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1))
    return address_repository

def test_get_all_addresses(test_addresses):
    addresses = test_addresses.get_all()
    assert len(addresses) == 4

def test_add_and_retrieve_address(address_repository, test_session):
    created_at = datetime.utcnow()
    new_address = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1)
    address_repository.add(new_address)
    test_session.commit()

    retrieved_address = address_repository.get_by_id(new_address.id)
    assert retrieved_address is not None
    assert retrieved_address.address_line_1 == "123 Main St"
    assert retrieved_address.city == "Anytown"
    assert retrieved_address.state == "NY"
    assert retrieved_address.zip_code == "12345"
    assert retrieved_address.created_at is not None
    assert retrieved_address.created_by == "system"
    
def test_update_address(address_repository, test_session):
    address = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1)
    address_repository.add(address)
    test_session.commit()

    retrieved_address = address_repository.get_by_id(address.id)
    retrieved_address.address_line_1 = "456 Main St"
    address_repository.update(retrieved_address)
    test_session.commit()

    updated_address = address_repository.get_by_id(address.id)
    assert updated_address is not None
    assert updated_address.address_line_1 == "456 Main St"
    assert updated_address.city == "Anytown"
    assert updated_address.state == "NY"
    assert updated_address.zip_code == "12345"
    assert updated_address.created_at is not None
    assert updated_address.created_by == "system"
    assert updated_address.updated_at is not None
    assert updated_address.updated_by == "system"
    
def test_update_address_with_nonexistent_address(address_repository, test_session):
    address = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1)
    with pytest.raises(ValueError):
        address_repository.update(address)    
            
def test_update_address_raises_exception(address_repository, mocker):
    address = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1)
    address_repository.add(address)
    mocker.patch.object(address_repository.session, 'merge', side_effect=Exception('Test Exception'))
    
    with pytest.raises(Exception):
        address_repository.update(address)

def test_delete_address(address_repository, test_session):
    address_to_delete = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1, created_by="test", created_at=datetime.utcnow())
    address_repository.add(address_to_delete)
    test_session.commit()

    address_repository.delete(address_to_delete)
    test_session.commit()

    deleted_address = address_repository.get_by_id(address_to_delete.id)
    assert deleted_address is None

def test_delete_nonexistent_address(address_repository):
    address_to_delete = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1, created_by="test", created_at=datetime.utcnow())
    with pytest.raises(ValueError):
        address_repository.delete(address_to_delete)

def test_delete_address_raises_exception(address_repository, mocker):
    address_to_delete = Address(address_line_1="123 Main St", city="Anytown", state="NY", zip_code="12345", person_id=1, created_by="test", created_at=datetime.utcnow())
    address_repository.add(address_to_delete)
    mocker.patch.object(address_repository.session, 'delete', side_effect=Exception('Test Exception'))
    
    with pytest.raises(Exception):
        address_repository.delete(address_to_delete)
  