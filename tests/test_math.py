import pytest
import pacer_py.math as pp_math


def test_duration_to_hh_mm_ss() -> None:
    assert pp_math.duration_to_hh_mm_ss(1.5, 'h') == (1, 30, 0)
    assert pp_math.duration_to_hh_mm_ss(90, 'min') == (1, 30, 0)
    assert pp_math.duration_to_hh_mm_ss(3600, 'sec') == (1, 0, 0)
    assert pp_math.duration_to_hh_mm_ss(0.5, 'h') == (0, 30, 0)
    assert pp_math.duration_to_hh_mm_ss(45.5, 'min') == (0, 45, 30)
    assert pp_math.duration_to_hh_mm_ss(3661, 'sec') == (1, 1, 1)
    assert pp_math.duration_to_hh_mm_ss(0, 'h') == (0, 0, 0)
    assert pp_math.duration_to_hh_mm_ss(0, 'min') == (0, 0, 0)
    assert pp_math.duration_to_hh_mm_ss(0, 'sec') == (0, 0, 0)


def test_duration_to_hh_mm_ss_invalid_unit() -> None:
    with pytest.raises(ValueError):
        pp_math.duration_to_hh_mm_ss(1.5, 'days')
    with pytest.raises(ValueError):
        pp_math.duration_to_hh_mm_ss(90, 'weeks')
    with pytest.raises(ValueError):
        pp_math.duration_to_hh_mm_ss(3600, 'months')
    with pytest.raises(ValueError):
        pp_math.duration_to_hh_mm_ss(100, 'years')


def test_pace_from_duration_and_distance() -> None:
    assert pp_math.pace_from_duration_and_distance(360, 1000, 'min/km') == 6.0
    assert pp_math.pace_from_duration_and_distance(300, 1000, 'min/km') == 5.0
    assert pp_math.pace_from_duration_and_distance(60, 100, 'sec/m') == 0.6
    assert pp_math.pace_from_duration_and_distance(120, 200, 'sec/m') == 0.6
    assert pp_math.pace_from_duration_and_distance(1500, 5000, 'min/km') == 5.0


def test_pace_from_duration_and_distance_invalid_distance() -> None:
    with pytest.raises(ValueError):
        pp_math.pace_from_duration_and_distance(300, 0, 'min/km')
    with pytest.raises(ValueError):
        pp_math.pace_from_duration_and_distance(300, -100, 'sec/m')


def test_pace_from_duration_and_distance_invalid_format() -> None:
    with pytest.raises(ValueError):
        pp_math.pace_from_duration_and_distance(300, 1000, 'hours/mile')
    with pytest.raises(ValueError):
        pp_math.pace_from_duration_and_distance(300, 1000, 'min/mile')


def test_duration_from_pace_and_distance() -> None:
    assert pp_math.duration_from_pace_and_distance(0.006, 1000) == 6.0
    assert pp_math.duration_from_pace_and_distance(0.005, 1000) == 5.0
    assert pp_math.duration_from_pace_and_distance(0.6, 100) == 60.0
    assert pp_math.duration_from_pace_and_distance(0.6, 200) == 120.0
    assert pp_math.duration_from_pace_and_distance(0.005, 5000) == 25.0


def test_duration_from_pace_and_distance_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        pp_math.duration_from_pace_and_distance(0.0, 10)
    with pytest.raises(ValueError):
        pp_math.duration_from_pace_and_distance(0.005, -100)


def test_distance_from_pace_and_duration() -> None:
    assert pp_math.distance_from_pace_and_duration(0.006, 6.0, 'm') == 1000.0
    assert pp_math.distance_from_pace_and_duration(0.005, 5.0, 'km') == 1.0
    assert pp_math.distance_from_pace_and_duration(0.6, 60.0, 'm') == 100.0
    assert pp_math.distance_from_pace_and_duration(0.6, 120.0, 'm') == 200.0
    assert pp_math.distance_from_pace_and_duration(0.005, 25.0, 'km') == 5.0


def test_distance_from_pace_and_duration_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        pp_math.distance_from_pace_and_duration(0, 1000, 'm')
    with pytest.raises(ValueError):
        pp_math.distance_from_pace_and_duration(-0.5, 1000, 'm')
    with pytest.raises(ValueError):
        pp_math.distance_from_pace_and_duration(0.005, -1000, 'm')


def test_distance_from_pace_and_duration_invalid_unit() -> None:
    with pytest.raises(ValueError):
        pp_math.distance_from_pace_and_duration(0.005, 1000, 'yards')
    with pytest.raises(ValueError):
        pp_math.distance_from_pace_and_duration(0.005, 1000, 'miles')
