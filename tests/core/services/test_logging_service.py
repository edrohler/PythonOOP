import pytest
from src.core.services.logging_service import LoggingService
from unittest.mock import patch

@pytest.fixture
def mock_file_handler(mocker):
    with patch('logging.FileHandler') as mock:
        yield mock

@pytest.fixture
def logging_service(mock_file_handler):
    return LoggingService('TestLogger')

def test_log_info(logging_service):
    with patch.object(logging_service.logger, 'info') as mock_info:
        logging_service.log_info("Test info message")
        mock_info.assert_called_once_with("Test info message")

def test_log_error(logging_service):
    with patch.object(logging_service.logger, 'error') as mock_error:
        logging_service.log_error("Test error message")
        mock_error.assert_called_once_with("Test error message")

def test_log_warning(logging_service):
    with patch.object(logging_service.logger, 'warning') as mock_warning:
        logging_service.log_warning("Test warning message")
        mock_warning.assert_called_once_with("Test warning message")

def test_log_debug(logging_service):
    with patch.object(logging_service.logger, 'debug') as mock_debug:
        logging_service.log_debug("Test debug message")
        mock_debug.assert_called_once_with("Test debug message")

def test_singleton_behavior():
    service1 = LoggingService('TestLogger')
    service2 = LoggingService('TestLogger')
    assert service1 is service2
