""" Testing the smoot function """
import pytest
from unit_curious.unit_curious import smoot

def test_default_conversion():
    result = smoot(1)  # Test with smoot value of 1
    assert result == 5.58333


def test_meter_conversion():
    result = smoot(1, to="meter")
    assert result == 1.7018


def test_inches_conversion():
    result = smoot(1, to="inches")
    assert result == 67.0


def test_invalid_unit():
    with pytest.raises(ValueError):
        smoot(1, to="cubit")  # Unsupported unit
