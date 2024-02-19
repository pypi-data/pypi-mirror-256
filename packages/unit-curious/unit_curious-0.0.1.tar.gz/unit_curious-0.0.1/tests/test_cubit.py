""" Testing the cubit function """
import pytest
from unit_curious.unit_curious import cubit

def test_cubit_foot():
    """Testing the cubit function for to = 'foot'"""
    dictionary = {
        cubit(5): 7.5,
        cubit(23): 34.5,
    }
    for key, value in dictionary.items():
        assert key == value

def test_cubit_meter():
    """Testing the cubit function for to = 'meter'"""
    dictionary = {
        cubit(13, to="meter"): 6.9342,
        cubit(34, to="meter"): 18.1356,
    }
    for key, value in dictionary.items():
        assert key == value


def test_cubit_conversion():
    # Test conversion to foot
    assert cubit(2) == 3.0
    assert cubit(3, to="foot") == 4.5

    # Test conversion to meter
    assert cubit(2, to="meter") == 1.0668
    assert cubit(3, to="meter") == 1.6002

    # Test conversion to inches
    assert cubit(2, to="inches") == 35.433070866142
    assert cubit(3, to="inches") == 53.149606299213005


def test_invalid_unit():
    with pytest.raises(ValueError, match="Invalid unit. Available options: foot, meter, or inches"):
        cubit(2, to="invalid_unit")

