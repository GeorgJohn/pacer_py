import pytest
from pacer_py.utils import float_to_duration


def test_float_to_duration() -> None:
    assert float_to_duration(1.5, 'h') == (1, 30, 0)
    assert float_to_duration(90, 'min') == (1, 30, 0)
    assert float_to_duration(3600, 'sec') == (1, 0, 0)
    assert float_to_duration(0.5, 'h') == (0, 30, 0)
    assert float_to_duration(45.5, 'min') == (0, 45, 30)
    assert float_to_duration(3661, 'sec') == (1, 1, 1)
    assert float_to_duration(0, 'h') == (0, 0, 0)
    assert float_to_duration(0, 'min') == (0, 0, 0)
    assert float_to_duration(0, 'sec') == (0, 0, 0)


def test_float_to_duration_invalid_unit() -> None:
    with pytest.raises(ValueError):
        float_to_duration(1.5, 'days')
    with pytest.raises(ValueError):
        float_to_duration(90, 'weeks')
    with pytest.raises(ValueError):
        float_to_duration(3600, 'months')
    with pytest.raises(ValueError):
        float_to_duration(100, 'years')