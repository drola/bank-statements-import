import datetime
import unittest
from decimal import Decimal

import fixtures
from delavska_hranilnica import _parse_date, _parse_amount, TransactionsExport


class DelavskaHranilnicaTestCase(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(datetime.date(2021, 12, 23), _parse_date("23.12.2021"))

        with self.assertRaises(ValueError):
            _parse_date("unexpected")

    def test_parse_amount(self):
        self.assertEqual(Decimal('12345.00'), _parse_amount('12345'))
        self.assertEqual(Decimal('12345.60'), _parse_amount('12345,6'))
        self.assertEqual(Decimal('12345.67'), _parse_amount('12.345,67'))
        self.assertEqual(Decimal('12345.678'), _parse_amount('12.345,678'))
        self.assertEqual(None, _parse_amount(''))

    def test_from_file(self):
        self.assertEqual(fixtures.delavska_hranilnica_transactions_export,
                         TransactionsExport.from_file(fixtures.test_delavska_hranilnica_csv))


if __name__ == '__main__':
    unittest.main()
