import pytest

from pacer_py.user_input_parser import (
    parse_duration, 
    parse_distance, 
    parse_option
)


def test_parse_duration() -> None:

    assert parse_duration("01:02:03") == 3723
    assert parse_duration("02:03") == 123
    assert parse_duration("45") == 45
    assert parse_duration("00:00:30") == 30
    assert parse_duration("1:00") == 60
    assert parse_duration("0:45") == 45
    assert parse_duration("10:00:00") == 36000
    assert parse_duration("0:0:5") == 5
    assert parse_duration("5") == 5
    assert parse_duration("0:5") == 5
    assert parse_duration("0:0:0") == 0
    assert parse_duration("1234") == 1234
    assert parse_duration("61:00") == 61 * 60
    assert parse_duration("25:00:00") == 25 * 3600


def test_parse_duration_invalid_character() -> None:

    with pytest.raises(ValueError):
        parse_duration("invalid")

    with pytest.raises(ValueError):
        parse_duration("1:2:3:4")

    with pytest.raises(ValueError):
        parse_duration("1::2")

    with pytest.raises(ValueError):
        parse_duration("1:2:three")

    with pytest.raises(ValueError):
        parse_duration("-2:17:18")

    with pytest.raises(ValueError):
        parse_duration("17:-18")

    with pytest.raises(ValueError):
        parse_duration("-42")

def test_parse_duration_invalid_values() -> None:

    with pytest.raises(ValueError):
        parse_duration("01:67:15")
    
    with pytest.raises(ValueError):
        parse_duration("25:61:05")

    with pytest.raises(ValueError):
        parse_duration("17:67")


def test_parse_distance_valid_inputs() -> None:
    """Test parse_distance with valid inputs."""
    
    # Test kilometers
    assert parse_distance("5km") == 5000.0
    assert parse_distance("1.5km") == 1500.0
    assert parse_distance("0.5km") == 500.0
    assert parse_distance("10km") == 10000.0
    
    # Test k shorthand
    assert parse_distance("5k") == 5000.0
    assert parse_distance("2.5k") == 2500.0
    
    # Test meters
    assert parse_distance("500m") == 500.0
    assert parse_distance("100.5m") == 100.5
    assert parse_distance("0m") == 0.0
    
    # Test with whitespace
    assert parse_distance(" 5km ") == 5000.0
    assert parse_distance("  3.5k  ") == 3500.0
    
    # Test case insensitive
    assert parse_distance("5KM") == 5000.0
    assert parse_distance("2K") == 2000.0
    assert parse_distance("100M") == 100.0

def test_parse_distance_predefined() -> None:

    # Test Marathon
    assert parse_distance("marathon") == 42195.0
    assert parse_distance("Marathon") == 42195.0
    assert parse_distance("MARATHON") == 42195.0
    assert parse_distance("MRT") == 42195.0

    # Test Half Marathon
    assert parse_distance("half marathon") == 21097.5
    assert parse_distance("Half-Marathon") == 21097.5
    assert parse_distance("HALF MARATHON") == 21097.5
    assert parse_distance("HMT") == 21097.5
    assert parse_distance("HM") == 21097.5
    assert parse_distance("semi marathon") == 21097.5
    assert parse_distance("Semi Marathon") == 21097.5
    assert parse_distance("SEMI-MARATHON") == 21097.5

def test_parse_distance_invalid_inputs() -> None:
    """Test parse_distance with invalid inputs."""
    
    # Test invalid units
    with pytest.raises(ValueError, match="can't be parsed to a distance"):
        parse_distance("5miles")
    
    with pytest.raises(ValueError, match="can't be parsed to a distance"):
        parse_distance("5")
    
    with pytest.raises(ValueError, match="can't be parsed to a distance"):
        parse_distance("5ft")
    
    # Test invalid numeric values
    with pytest.raises(ValueError, match="invalid numeric value"):
        parse_distance("abckm")
    
    with pytest.raises(ValueError, match="invalid numeric value"):
        parse_distance("5.5.5km")
    
    with pytest.raises(ValueError, match="invalid numeric value"):
        parse_distance("--5km")
    
    # Test negative values
    with pytest.raises(ValueError, match="Distance cannot be negative"):
        parse_distance("-5km")
    
    with pytest.raises(ValueError, match="Distance cannot be negative"):
        parse_distance("-2.5m")
    
    # Test empty numeric part
    with pytest.raises(ValueError, match="contains no numeric value"):
        parse_distance("km")
    
    with pytest.raises(ValueError, match="contains no numeric value"):
        parse_distance("m")
    
    # Test empty string
    with pytest.raises(ValueError):
        parse_distance("")
    
    with pytest.raises(ValueError):
        parse_distance("   ")


def test_parse_option_valid() -> None:
    options = {1: "Option 1", 2: "Option 2", 3: "Option 3"}
    
    assert parse_option("1", options) == 1
    assert parse_option("2", options) == 2
    assert parse_option("3", options) == 3
    assert parse_option(" 1 ", options) == 1  # Test with whitespace


def test_parse_option_invalid() -> None:
    options = {1: "Option 1", 2: "Option 2", 3: "Option 3"}
    
    with pytest.raises(ValueError, match="is not a valid option"):
        parse_option("4", options)
    
    with pytest.raises(ValueError, match="is not a valid option"):
        parse_option("0", options)

    with pytest.raises(ValueError, match="is not a valid number"):
        parse_option("-1", options)
    
    with pytest.raises(ValueError, match="is not a valid number"):
        parse_option("abc", options)

    with pytest.raises(ValueError, match="is not a valid number"):
        parse_option("1.5", options)

    with pytest.raises(ValueError, match="is not a valid number"):
        parse_option("", options)
