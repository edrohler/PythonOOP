import pytest
from src.core.services.logging_service import LoggingService
from unittest.mock import patch

def test_log_info(mock_logger):
    with patch.object(mock_logger, 'log_info') as mock_info:
        mock_logger.log_info("Test info message")
        mock_info.assert_called_once_with("Test info message")

def test_log_error(mock_logger):
    with patch.object(mock_logger.logger, 'error') as mock_error:
        mock_logger.log_error("Test error message")
        mock_error.assert_called_once_with("Test error message")

def test_log_warning(mock_logger):
    with patch.object(mock_logger.logger, 'warning') as mock_warning:
        mock_logger.log_warning("Test warning message")
        mock_warning.assert_called_once_with("Test warning message")

def test_log_debug(mock_logger):
    with patch.object(mock_logger.logger, 'debug') as mock_debug:
        mock_logger.log_debug("Test debug message")
        mock_debug.assert_called_once_with("Test debug message")

def test_singleton_behavior(mock_logger):
    another_service = LoggingService.get_instance('TestLogger')
    assert mock_logger is another_service
