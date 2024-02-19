""" Testing the stone function """
import pytest
from unit_curious.unit_curious import stone


def test_default_conversion():
    result = stone(1)  # Test with a stone value of 1
    assert result == 6.35029


def test_pounds_conversion():
    result = stone(1, to="Pound")
    assert result == 14


def test_grams_conversion():
    result = stone(1, to="Gram")
    assert result == 6350.29


def test_ounces_conversion():
    result = stone(1, to="Ounces")
    assert result == 224


def test_invalid_unit():
    with pytest.raises(ValueError):
        stone(1, to="cubit")  # Unsupported unit
