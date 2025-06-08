import os
import sys

# Ensure the project src/python directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))

from metagame.utils.numbers import is_integer


def test_integer_strings():
    assert is_integer("10") is True
    assert is_integer("-3") is True


def test_non_integer_strings():
    assert is_integer("10.5") is False
    assert is_integer("abc") is False


def test_numeric_types():
    assert is_integer(5) is True
    assert is_integer(3.0) is True
