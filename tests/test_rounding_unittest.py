import unittest
from decimal import Decimal, InvalidOperation
from math import inf, nan

from rounding import safe_round


class TestSafeRound_UnitTest(unittest.TestCase):
    # --- Core banker's rounding (half-to-even) ---
    def test_half_to_even_core(self):
        self.assertEqual(safe_round(2.5), 2)     # 2 is even
        self.assertEqual(safe_round(3.5), 4)     # 4 is even
        self.assertEqual(safe_round(-1.5), -2)   # -2 is even

    # --- ndigits >= 0 ---
    def test_ndigits_positive(self):
        self.assertAlmostEqual(safe_round(1.25, 1), 1.2)               # 12.5 -> 12
        self.assertEqual(safe_round(Decimal("1.25"), 1), Decimal("1.2"))

    # --- ndigits < 0 (tens, hundreds…) ---
    def test_ndigits_negative(self):
        self.assertEqual(safe_round(25, -1), 20)   # 20 is even
        self.assertEqual(safe_round(35, -1), 40)

    # --- Decimal exact halves & tricky decimals ---
    def test_decimal_exact(self):
        self.assertEqual(safe_round(Decimal("2.675"), 2), Decimal("2.68"))
        self.assertEqual(safe_round(Decimal("2.5")), 2)

    # --- Float binary representation quirk ---
    def test_float_binary_quirk(self):
        # 2.675 isn't exactly representable; CPython yields 2.67
        self.assertAlmostEqual(safe_round(2.675, 2), 2.67)

    # --- Large & zero ---
    def test_large_and_zero(self):
        self.assertEqual(safe_round(0.0), 0)
        self.assertEqual(safe_round(123456789.5), 123456790)

    # --- Type validation errors ---
    def test_type_errors(self):
        with self.assertRaises(TypeError):
            safe_round("bad")                        # x type
        with self.assertRaises(TypeError):
            safe_round(1.2, ndigits=1.5)            # ndigits type

    # --- Special float values: inf / nan ---
    def test_inf_nan_float_behavior(self):
        # ndigits is None -> int conversion => exceptions
        with self.assertRaises(OverflowError):
            safe_round(inf)
        with self.assertRaises(OverflowError):
            safe_round(-inf)
        with self.assertRaises(ValueError):
            safe_round(nan)
        # ndigits provided -> values propagate
        self.assertEqual(safe_round(inf, 0), inf)
        self.assertEqual(safe_round(-inf, 3), -inf)
        self.assertTrue(str(safe_round(nan, 2)) == "nan")

    # --- Special Decimal values: NaN / Infinity ---
    def test_inf_nan_decimal_behavior(self):
        with self.assertRaises(ValueError):
            safe_round(Decimal("NaN"))
        with self.assertRaises(OverflowError):
            safe_round(Decimal("Infinity"))
        # With ndigits set, Decimal("NaN") propagates, Infinity raises InvalidOperation
        self.assertTrue(safe_round(Decimal("NaN"), 2).is_nan())
        with self.assertRaises(InvalidOperation):
            safe_round(Decimal("Infinity"), 0)


if __name__ == "__main__":
    unittest.main()
