"""Unit tests for safe_round using unittest."""

import unittest
from decimal import Decimal, InvalidOperation
from math import inf, nan

from rounding import safe_round


class TestSafeRoundUnitTest(unittest.TestCase):
    """Test suite verifying banker's rounding and edge cases for safe_round."""

    def test_half_to_even_core(self):
        """Round halves to nearest even integer (banker's rounding)."""
        self.assertEqual(safe_round(2.5), 2)
        self.assertEqual(safe_round(3.5), 4)
        self.assertEqual(safe_round(-1.5), -2)

    def test_ndigits_positive(self):
        """Round to a positive number of fractional digits."""
        self.assertAlmostEqual(safe_round(1.25, 1), 1.2)
        self.assertEqual(safe_round(Decimal("1.25"), 1), Decimal("1.2"))

    def test_ndigits_negative(self):
        """Round with negative ndigits (tens, hundreds, ...)."""
        self.assertEqual(safe_round(25, -1), 20)
        self.assertEqual(safe_round(35, -1), 40)

    def test_decimal_exact(self):
        """Check exact Decimal halves and tricky values."""
        self.assertEqual(safe_round(Decimal("2.675"), 2), Decimal("2.68"))
        self.assertEqual(safe_round(Decimal("2.5")), 2)

    def test_float_binary_quirk(self):
        """Document binary float representation effect on 2.675."""
        self.assertAlmostEqual(safe_round(2.675, 2), 2.67)

    def test_large_and_zero(self):
        """Round zeros and large values."""
        self.assertEqual(safe_round(0.0), 0)
        self.assertEqual(safe_round(123456789.5), 123456790)

    def test_type_errors(self):
        """Reject invalid argument types."""
        with self.assertRaises(TypeError):
            safe_round("bad")
        with self.assertRaises(TypeError):
            safe_round(1.2, ndigits=1.5)

    def test_inf_nan_float_behavior(self):
        """Validate float infinities/NaN behavior with/without ndigits."""
        with self.assertRaises(OverflowError):
            safe_round(inf)
        with self.assertRaises(OverflowError):
            safe_round(-inf)
        with self.assertRaises(ValueError):
            safe_round(nan)
        self.assertEqual(safe_round(inf, 0), inf)
        self.assertEqual(safe_round(-inf, 3), -inf)
        self.assertTrue(str(safe_round(nan, 2)) == "nan")

    def test_inf_nan_decimal_behavior(self):
        """Validate Decimal NaN/Infinity behavior with/without ndigits."""
        with self.assertRaises(ValueError):
            safe_round(Decimal("NaN"))
        with self.assertRaises(OverflowError):
            safe_round(Decimal("Infinity"))
        self.assertTrue(safe_round(Decimal("NaN"), 2).is_nan())
        with self.assertRaises(InvalidOperation):
            safe_round(Decimal("Infinity"), 0)


if __name__ == "__main__":
    unittest.main()
