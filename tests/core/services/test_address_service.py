from src.core.services.address_service import AddressService
from src.core.domain.models.address import Address

def test_get_address_by_id(mock_unit_of_work, mocker):
    # Arrange
    address_service = AddressService(mock_unit_of_work)
    address_id = 1
    mock_get_by_id = mocker.patch.object(mock_unit_of_work.address_repository, "get_by_id")
    mock_get_by_id.return_value = Address(id=1, address_line_1="123 Main St", address_line_2="", city="New York", state="NY", zip_code="10001", person_id=1)
    
    # Act
    result = address_service.get_address_by_id(address_id)
    
    # Assert
    assert isinstance(result, Address)
    assert result.id == address_id
    
def test_get_all_addresses(mock_unit_of_work, mocker):
    # Arrange
    address_service = AddressService(mock_unit_of_work)
    mock_get_all = mocker.patch.object(mock_unit_of_work.address_repository, "get_all")
    mock_get_all.return_value = [Address(id=1, address_line_1="123 Main St", address_line_2="", city="New York", state="NY", zip_code="10001", person_id=1)]
    
    # Act
    result = address_service.get_all_addresses()
    
    # Assert
    assert isinstance(result, list)
    assert all(isinstance(address, Address) for address in result)
    
def test_create_address(mock_unit_of_work, mocker):
    # Arrange
    address_service = AddressService(mock_unit_of_work)
    address = Address(id=1, address_line_1="123 Main St", address_line_2="", city="New York", state="NY", zip_code="10001", person_id=1)
    mocker_add = mocker.patch.object(mock_unit_of_work.address_repository, "add")
    mocker_add.return_value = None
    
    # Act
    address_service.create_address(address)
    
    # Assert
    mock_unit_of_work.address_repository.add.assert_called_once()
    
def test_update_address(mock_unit_of_work, mocker):
    # Arrange
    address_service = AddressService(mock_unit_of_work)
    address = Address(id=1, address_line_1="123 Main St", address_line_2="", city="New York", state="NY", zip_code="10001", person_id=1)
    mocker_update = mocker.patch.object(mock_unit_of_work.address_repository, "update")
    mocker_update.return_value = None
    
    # Act
    address_service.update_address(address)
    
    # Assert
    mock_unit_of_work.address_repository.update.assert_called_once()
    
def test_delete_address(mock_unit_of_work, mocker):
    # Arrange
    address_service = AddressService(mock_unit_of_work)
    address_id = 1
    mocker_delete = mocker.patch.object(mock_unit_of_work.address_repository, "delete")
    mocker_delete.return_value = None
    
    # Act
    address_service.delete_address(address_id)
    
    # Assert
    mock_unit_of_work.address_repository.delete.assert_called_once()