"""Pytest tests for safe_round (parametrized)."""

import math
from decimal import Decimal, InvalidOperation

import pytest
from rounding import safe_round


def test_parametrized_core():
    """Core rounding behavior across cases."""
    cases = [
        (2.5, None, 2),
        (3.5, None, 4),
        (-1.5, None, -2),
        (1.25, 1, 1.2),
        (Decimal("1.25"), 1, Decimal("1.2")),
        (25, -1, 20),
        (35, -1, 40),
        (0.0, None, 0),
        (123456789.5, None, 123456790),
    ]
    for x, nd, expected in cases:
        if nd is None:
            assert safe_round(x) == expected
        else:
            assert safe_round(x, nd) == expected


def test_decimal_exact_half_even():
    """Exact Decimal halves follow half-to-even."""
    assert safe_round(Decimal("2.675"), 2) == Decimal("2.68")
    assert safe_round(Decimal("2.5")) == 2


def test_float_binary_quirk():
    """Binary float quirk for 2.675 at 2 digits."""
    assert safe_round(2.675, 2) == pytest.approx(2.67)


def test_type_errors():
    """Invalid argument types raise TypeError."""
    with pytest.raises(TypeError):
        safe_round("bad", None)
    with pytest.raises(TypeError):
        safe_round(1.2, 1.5)


def test_float_inf_nan_behavior():
    """Float inf/-inf/NaN behavior mirrors built-in round."""
    with pytest.raises(OverflowError):
        safe_round(math.inf)
    with pytest.raises(OverflowError):
        safe_round(-math.inf)
    with pytest.raises(ValueError):
        safe_round(math.nan)

    assert safe_round(math.inf, 0) == math.inf
    assert safe_round(-math.inf, 4) == -math.inf
    assert math.isnan(safe_round(math.nan, 2))


def test_decimal_inf_nan_behavior():
    """Decimal NaN/Infinity behavior mirrors built-in round."""
    with pytest.raises(ValueError):
        safe_round(Decimal("NaN"))
    with pytest.raises(OverflowError):
        safe_round(Decimal("Infinity"))

    assert safe_round(Decimal("NaN"), 2).is_nan()
    with pytest.raises(InvalidOperation):
        safe_round(Decimal("Infinity"), 2)
