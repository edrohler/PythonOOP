import pytest
import argparse
from unittest.mock import patch, call
import sys
sys.path.insert(0, './src')
from src.main import main

@patch('argparse.ArgumentParser.parse_args')
@patch('src.main.app.run')
def test_main_api_serve_prod(mock_run, mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(serve=True, debug=False)
    main()
    mock_run.assert_called_once_with(debug=False, use_reloader=False)
    
@patch('src.main.app.run')
@patch('argparse.ArgumentParser.parse_args')
def test_main_api_serve_debug(mock_parse_args, mock_run):
    mock_parse_args.return_value = argparse.Namespace(serve=True, debug=True)
    main()
    mock_run.assert_called_once_with(debug=True, use_reloader=True)