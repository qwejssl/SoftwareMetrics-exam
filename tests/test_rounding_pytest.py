import math
import pytest
from decimal import Decimal, InvalidOperation
from rounding import safe_round


@pytest.mark.parametrize(
    "x, nd, expected",
    [
        (2.5, None, 2),
        (3.5, None, 4),
        (-1.5, None, -2),
        (1.25, 1, 1.2),
        (Decimal("1.25"), 1, Decimal("1.2")),
        (25, -1, 20),
        (35, -1, 40),
        (0.0, None, 0),
        (123456789.5, None, 123456790),
    ],
)
def test_parametrized_core(x, nd, expected):
    if nd is None:
        assert safe_round(x) == expected
    else:
        assert safe_round(x, nd) == expected


def test_decimal_exact_half_even():
    assert safe_round(Decimal("2.675"), 2) == Decimal("2.68")
    assert safe_round(Decimal("2.5")) == 2


def test_float_binary_quirk():
    # Use approx due to binary fp representation
    assert safe_round(2.675, 2) == pytest.approx(2.67)


@pytest.mark.parametrize("bad, nd", [("bad", None), (1.2, 1.5)])
def test_type_errors(bad, nd):
    with pytest.raises(TypeError):
        safe_round(bad, nd)


def test_float_inf_nan_behavior():
    # ndigits None -> exceptions
    with pytest.raises(OverflowError):
        safe_round(math.inf)
    with pytest.raises(OverflowError):
        safe_round(-math.inf)
    with pytest.raises(ValueError):
        safe_round(math.nan)

    # ndigits present -> values propagate
    assert safe_round(math.inf, 0) == math.inf
    assert safe_round(-math.inf, 4) == -math.inf
    res = safe_round(math.nan, 2)
    assert math.isnan(res)


def test_decimal_inf_nan_behavior():
    with pytest.raises(ValueError):
        safe_round(Decimal("NaN"))
    with pytest.raises(OverflowError):
        safe_round(Decimal("Infinity"))
    # With ndigits, Decimal NaN propagates, Infinity raises InvalidOperation
    assert safe_round(Decimal("NaN"), 2).is_nan()
    with pytest.raises(InvalidOperation):
        safe_round(Decimal("Infinity"), 2)
