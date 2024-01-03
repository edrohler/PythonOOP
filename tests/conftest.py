from unittest.mock import patch
import pytest

from src.core.services.logging_service import LoggingService
from src.infrastructure.database import DatabaseConfig

@pytest.fixture
def mock_file_handler(mocker):
    with patch('logging.FileHandler') as mock:
        yield mock

@pytest.fixture
def mock_logger(mocker):
    return LoggingService.get_instance('TestLogger')

@pytest.fixture
def mock_database_config(mock_logger):
    # Function-scoped fixture that uses a mock logger
    return DatabaseConfig('sqlite:///:memory:', echo=False, logger=mock_logger)

@pytest.fixture
def test_database_config(mocker, mock_database_config):
    # Setup a test database configuration
    test_config = mock_database_config
    test_config.init_db()
    return test_config

@pytest.fixture
def test_session(test_database_config):
    # Create a new session for testing
    return test_database_config.get_session()