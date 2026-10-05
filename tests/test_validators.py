import pytest
from validators import get_valid_integer, get_valid_float, get_valid_name

def test_get_valid_integer(monkeypatch):
    # Test valid input immediately
    monkeypatch.setattr('builtins.input', lambda _: "42")
    assert get_valid_integer("Enter an integer: ", 0, 100) == 42

    # Test invalid input followed by valid input
    inputs = iter(["abc", "3.14", "99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_valid_integer("Enter an integer: ", 0, 100) == 99

    # Test rejects value below minimum
    inputs = iter(["0", "50"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_valid_integer("Enter an integer: ", 1, 100) == 50

    # Test rejects value above maximum
    inputs = iter(["101", "100"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_valid_integer("Enter an integer: ", 1, 100) == 100

def test_get_valid_float(monkeypatch):
    # Test valid float
    monkeypatch.setattr('builtins.input', lambda _: "85.5")
    assert get_valid_float("Enter a float: ", 0, 100) == 85.5

    # Test valid integer representation
    monkeypatch.setattr('builtins.input', lambda _: "90")
    assert get_valid_float("Enter a float: ", 0, 100) == 90.0

    # Test invalid input followed by valid input
    inputs = iter(["xyz", "eighty", "72.3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_valid_float("Enter a float: ", 0, 100) == 72.3

    # Test rejects value below minimum
    inputs = iter(["-1", "0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_valid_float("Enter a float: ", 0, 100) == 0.0

    # Test rejects value above maximum
    inputs = iter(["101", "100"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_valid_float("Enter a float: ", 0, 100) == 100.0

def test_get_valid_name(monkeypatch):
    # Test valid name
    monkeypatch.setattr('builtins.input', lambda _: "Alice")
    assert get_valid_name("Enter name: ") == "Alice"

    # Test empty string then valid string
    inputs = iter(["", "   ", "Bob"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_valid_name("Enter name: ") == "Bob"

    # Test name with extra spaces
    monkeypatch.setattr('builtins.input', lambda _: "   Charlie   ")
    assert get_valid_name("Enter name: ") == "Charlie"
