from __future__ import annotations

from decimal import Decimal
from typing import Optional, Union, overload

Number = Union[int, float, Decimal]


@overload
def safe_round(x: Number) -> Number: ...
@overload
def safe_round(x: Number, ndigits: int) -> Number: ...


def safe_round(x: Number, ndigits: Optional[int] = None):
    """
    Validated wrapper around Python's built-in round(), keeping exact semantics
    (banker's rounding = half-to-even). Supports int, float, Decimal.

    Behavior mirrors built-in round:
      • round(x) with float('inf') or float('-inf') -> OverflowError
      • round(x) with float('nan') -> ValueError
      • round(x, n) with inf/-inf -> returns inf/-inf
      • round(x, n) with nan -> returns nan

      • round(Decimal('NaN')) -> ValueError (int conversion fails)
      • round(Decimal('Infinity')) -> OverflowError
      • round(Decimal('NaN'), n) -> Decimal('NaN')
      • round(Decimal('Infinity'), n) -> decimal.InvalidOperation (from context)

    We do not catch these; we let Python raise them (so coverage shows you hit
    exceptional paths in tests).
    """
    if ndigits is not None and not isinstance(ndigits, int):
        raise TypeError("ndigits must be an int or None")
    if not isinstance(x, (int, float, Decimal)):
        raise TypeError("x must be int, float, or Decimal")
    return round(x, ndigits) if ndigits is not None else round(x)
