""" Testing the barleycorm function """
import pytest
from unit_curious.unit_curious import barleycorn


def test_default_conversion():
    result = barleycorn(12)  # Test with sample value 12
    assert result == 0.3333336  # 12 barleycorns in feet


def test_meter_conversion():
    result = barleycorn(12, to="meter")
    assert result == 0.10160008127999999  # 12 barleycorns in meters


def test_inches_conversion():
    result = barleycorn(12, to="inches")
    assert result == 4.000003199999998  # 12 barleycorns in inches


def test_invalid_unit():
    with pytest.raises(ValueError):
        barleycorn(12, to="centimeter")  # Unsupported unit
