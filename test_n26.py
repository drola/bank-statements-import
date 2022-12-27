import unittest
from decimal import Decimal

from fixtures import test_n26_csv, n26_transactions
from n26 import _str_or_none, _parse_amount, Transaction


class N26TestCase(unittest.TestCase):
    def test_str_or_none(self):
        self.assertEqual("str", _str_or_none("str"))
        self.assertEqual(None, _str_or_none(""))
        self.assertEqual(None, _str_or_none("-"))

    def test_parse_amount(self):
        self.assertEqual(Decimal('123.45'), _parse_amount("123.45"))
        self.assertEqual(Decimal('123.456'), _parse_amount("123.456"))
        self.assertEqual(Decimal('-123.45'), _parse_amount("-123.45"))
        self.assertEqual(Decimal('123.40'), _parse_amount("123.4"))
        self.assertEqual(Decimal('-123.40'), _parse_amount("-123.4"))
        self.assertEqual(Decimal('123.00'), _parse_amount("123"))
        self.assertEqual(Decimal('-123.00'), _parse_amount("-123"))
        self.assertEqual(None, _parse_amount(""))

    def test_from_file(self):
        self.assertEqual(n26_transactions, Transaction.from_file(test_n26_csv))


if __name__ == '__main__':
    unittest.main()
