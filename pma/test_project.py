from project import (
    get_file_names,
    get_user_input,
    handle_error,
)


def test_get_file_names(monkeypatch):
    # Mock the command-line arguments
    monkeypatch.setattr("sys.argv", ["project.py", "custom_list.csv", "custom_prices.csv"])

    list_file, prices_file = get_file_names()

    assert list_file == "custom_list.csv"
    assert prices_file == "custom_prices.csv"


def test_get_file_names_without_arguments(monkeypatch):
    # Mock the command-line arguments
    monkeypatch.setattr("sys.argv", ["project.py"])

    list_file, prices_file = get_file_names()

    assert list_file == "ticker_list.csv"
    assert prices_file == "ticker_prices.csv"


def test_get_user_input(monkeypatch):
    # Mock the user input
    monkeypatch.setattr("builtins.input", lambda _: "3")

    choice = get_user_input()

    assert choice == 3


def test_handle_error(capsys):
    filename = "missing_file.csv"
    handle_error(FileNotFoundError(), filename)
    captured = capsys.readouterr()

    assert f"{filename} file not found." in captured.out


def test_handle_error_generic_error(capsys):
    filename = "data.csv"
    error_message = "An error occurred."
    handle_error(Exception(error_message), filename)
    captured = capsys.readouterr()

    assert f"An error occurred: {error_message}" in captured.out