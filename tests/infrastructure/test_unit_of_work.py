import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.unit_of_work import UnitOfWork
from src.infrastructure.repositories import AddressRepository, EmailRepository, PersonRepository

def test_unit_of_work(test_session, mock_database_config):
    # Act
    mock_database_config.get_session = MagicMock(return_value=test_session)
    uow = UnitOfWork(mock_database_config)
    
    # Assert
    assert isinstance(uow.address_repository, AddressRepository)
    assert isinstance(uow.email_repository, EmailRepository)
    assert isinstance(uow.person_repository, PersonRepository)
    assert uow.session is test_session

def test_unit_of_work_session_close(test_session, mock_database_config):
    # Act
    with patch('src.infrastructure.database.get_session', return_value=test_session), \
         patch.object(test_session, 'close') as mock_close, \
         patch.object(UnitOfWork, '__exit__') as mock_exit:
        with UnitOfWork(mock_database_config) as uow:
            pass
    
    # Assert
    mock_exit.assert_called_once()
    # mock_close.assert_called_once()