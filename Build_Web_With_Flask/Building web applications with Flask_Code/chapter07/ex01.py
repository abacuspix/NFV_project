# coding:utf-8

"""Doctest example"""

import doctest
import unittest


def sum_fnc(a, b):
    """
    Returns a + b

    >>> sum_fnc(10, 20)
    30
    >>> sum_fnc(-10, -20)
    -30
    >>> sum_fnc(10, -20)
    -10
    """
    return a + b


class TestSumFnc(unittest.TestCase):
    def test_sum_with_positive_numbers(self):
        result = sum_fnc(10, 20)
        self.assertEqual(result, 30)

    def test_sum_with_negative_numbers(self):
        result = sum_fnc(-10, -20)
        self.assertEqual(result, -30)

    def test_sum_with_mixed_signal_numbers(self):
        result = sum_fnc(10, -20)
        self.assertEqual(result, -10)


if __name__ == '__main__':
    doctest.testmod(verbose=1)
    unittest.main()
