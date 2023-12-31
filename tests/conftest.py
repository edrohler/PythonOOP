import pytest
from sqlalchemy.orm import Session

from src.infrastructure.database import DatabaseConfig

@pytest.fixture
def mock_session(mocker):
    return mocker.MagicMock(spec=Session)

@pytest.fixture(scope="module")
def test_database_config():
    # Setup a test database configuration
    test_config = DatabaseConfig('sqlite:///:memory:', echo=False)
    test_config.init_db()
    return test_config

@pytest.fixture(scope="module")
def test_session(test_database_config):
    # Create a new session for testing
    return test_database_config.get_session()