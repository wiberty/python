import pytest  # Unit testing
from project import (
    get_file_names,
    get_user_input,
    show_ticker_list,
    handle_error,
) as pr  # Functions tested


# Test get_file_names function default
def test_get_file_names():
    # Test default
    list_file, prices_file = get_file_names()
    assert list_file == "ticker_list.csv"
    assert prices_file == "ticker_prices.csv"


# Test get_file_names function custom values    
def test_get_file_names_custom():        
    sys.argv = ["random1.csv", "random2.csv", "random3.csv"]
    list_file, prices_file = get_file_names()
    assert list_file == "random1.csv"
    assert prices_file == "random2.csv"


# Test get_user_input function - valid
def test_get_user_input():
    input_values = ["1", "2", "3", "4", "5"]
    output_values = []
    def mock_input(s):
        output_values.append(s)
        return input_values.pop(0)
    pr.input = mock_input
    choice = get_user_input()
    assert choice == 1
    assert output_values == ["Enter your choice (1-5): "]

    
# Test get_user_input function - invalid
def test_get_user_input_invalid():
    input_values = ["0", "6", "a", "3"]
    output_values = []
    def mock_input(s):
        output_values.append(s)
        return input_values.pop(0)
    pr.input = mock_input
    choice = get_user_input()
    assert choice == 3
    assert output_values == [
        "Enter your choice (1-5): ",
        "Invalid choice. Please try again.",
        "Enter your choice (1-5): ",
    ]


# Test show_ticker_list function
def show_ticker_list(capsys):
    list_file = "ticker_list.csv"
    show_ticker_list(list_file)
    captured = capsys.readouterr()
    assert captured.out == "\nTicker List:\n"


# Test show_ticker_list function - file not found
def show_ticker_list_file_not_found(capsys):
    list_file = "nonexistent_ticker_list.csv"
    handle_error(FileNotFoundError(), list_file)
    captured = capsys.readouterr()
    assert captured.out == f"{list_file} file not found.\n"


# Test handle_error function messages
def test_handle_error(capsys):
    filename = "nonexistent_file.csv"

    handle_error(FileNotFoundError(), filename)
    captured = capsys.readouterr()
    assert captured.out == f"{filename} file not found.\n"

    handle_error(PermissionError(), filename)
    captured = capsys.readouterr()
    assert captured.out == f"Permission denied to access {filename} file.\n"

    error_message = "An error occurred"
    handle_error(Exception(error_message), filename)
    captured = capsys.readouterr()
    assert captured.out == f"An error occurred: {error_message}\n"