import pytest
from unittest.mock import mock_open, patch
from main import *
from cli_tutor.cli import process_string, process_file, main
from pathlib import Path


@pytest.mark.parametrize("input_sequence, expected_result", [
    ("abcabc", ""),
    ("aabbc", "c"),
    ("xyz", "xyz"),
    ("", ""),
])

def test_computing(input_sequence, expected_result):
    result = computing(input_sequence)
    assert result == expected_result

@pytest.fixture
def mock_print(mocker):
    return mocker.patch('builtins.print')

def test_process_string(mock_print):
    input_string = "Hello, World!"
    process_string(input_string)
    mock_print.assert_called_once_with(f"Processing string: {input_string}")

def test_process_file(mock_print, mocker):
    input_file = "txtfile.txt"
    input_path = Path(input_file)
    mocked_open = mocker.patch('builtins.open', new_callable=mock_open, read_data="File Content")
    process_file(input_path)
    mocked_open.assert_called_once_with(input_path, 'r')
    mock_print.assert_called_once_with("Processing file content: File Content")

def test_main_with_string_argument(mock_print, mocker):
    with mocker.patch('sys.argv', ['main.py', '--string', 'Hello, World!']):
        main()
        mock_print.assert_called_once_with("Processing string: Hello, World!")

def test_main_with_file_argument(mock_print, mocker):
    with mocker.patch('sys.argv', ['main.py', '--file', 'txtfile.txt']):
        mocked_open = mocker.patch('builtins.open', new_callable=mock_open, read_data="File Content")
        main()
        mocked_open.assert_called_once_with('txtfile.txt', 'r')
        mock_print.assert_called_once_with("Processing file content: File Content")

def test_main_without_arguments(mock_print, mocker):
    with mocker.patch('sys.argv', ['main.py']):
        main()
        mock_print.assert_called_once_with("Error: Either --string or --file must be specified.")

def test_main_with_both_arguments(mock_print, mocker):
    with mocker.patch('sys.argv', ['main.py', '--string', 'Hello, World!', '--file', 'txtfile.txt']):
        main()
        mock_print.assert_called_once_with("Error: Both --string and --file cannot be specified together. Please choose one.")


if __name__ == "__main__":
    pytest.main()
