from unittest.mock import MagicMock
from src.infrastructure.unit_of_work import UnitOfWork

def test_unit_of_work_singleton(mock_database_config, mock_logger):
    uow1 = UnitOfWork.get_instance(mock_database_config, mock_logger)
    uow2 = UnitOfWork.get_instance(mock_database_config, mock_logger)
    assert uow1 is uow2

def test_unit_of_work_initialization(mock_database_config, mock_logger):
    uow = UnitOfWork.get_instance(mock_database_config, mock_logger)
    assert uow.address_repository is not None
    assert uow.email_repository is not None
    assert uow.person_repository is not None

def test_unit_of_work_enter(mock_database_config, mock_logger):
    uow = UnitOfWork.get_instance(mock_database_config, mock_logger)
    with uow as entered_uow:
        assert entered_uow is uow
        # TODO: Check for logger messages

def test_unit_of_work_exit_session_closed(mock_database_config, mock_logger):
    # Reset UnitOfWork instance for a clean test environment
    UnitOfWork._instance = None

    # Mock the session object
    mock_session = MagicMock()
    mock_database_config.get_session = MagicMock(return_value=mock_session)

    # Create UnitOfWork instance
    uow = UnitOfWork.get_instance(mock_database_config, mock_logger)

    # Use the UnitOfWork instance in a context manager
    with uow:
        pass

    # Verify if the session's close method was called
    assert mock_session.close.called, "Session close method was not called"