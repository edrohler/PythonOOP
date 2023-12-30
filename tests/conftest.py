import pytest
from sqlalchemy.orm import Session

@pytest.fixture
def mock_session(mocker):
    return mocker.MagicMock(spec=Session)