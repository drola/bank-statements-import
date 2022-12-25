import datetime
import os.path
import unittest

from n26 import _str_or_none, _parse_amount, Transaction


class N26TestCase(unittest.TestCase):
    def test_str_or_none(self):
        self.assertEqual("str", _str_or_none("str"))
        self.assertEqual(None, _str_or_none(""))
        self.assertEqual(None, _str_or_none("-"))

    def test_parse_amount(self):
        self.assertEqual(12345, _parse_amount("123.45"))
        self.assertEqual(-12345, _parse_amount("-123.45"))
        self.assertEqual(12340, _parse_amount("123.4"))
        self.assertEqual(-12340, _parse_amount("-123.4"))
        self.assertEqual(12300, _parse_amount("123"))
        self.assertEqual(-12300, _parse_amount("-123"))
        self.assertEqual(None, _parse_amount(""))

        with self.assertRaises(AssertionError):
            _parse_amount("123.456")

    def test_from_file(self):
        self.assertEqual([Transaction(date=datetime.date(2022, 1, 12),
                                      payer_or_payee='SPOTIFY',
                                      payer_or_payee_account_number=None,
                                      transaction_type='MasterCard Payment',
                                      payment_reference=None,
                                      amount_eur=-599,
                                      amount_foreign_currency=-599,
                                      foreign_currency_type='EUR',
                                      exchange_rate=1.0),
                          Transaction(date=datetime.date(2022, 10, 4),
                                      payer_or_payee='Johnny',
                                      payer_or_payee_account_number='IT1234567890',
                                      transaction_type='MoneyBeam',
                                      payment_reference='The gift',
                                      amount_eur=-2000,
                                      amount_foreign_currency=None,
                                      foreign_currency_type=None,
                                      exchange_rate=None),
                          Transaction(date=datetime.date(2022, 12, 1),
                                      payer_or_payee='DIGITALOCEAN.COM',
                                      payer_or_payee_account_number=None,
                                      transaction_type='MasterCard Payment',
                                      payment_reference=None,
                                      amount_eur=-161,
                                      amount_foreign_currency=-166,
                                      foreign_currency_type='USD',
                                      exchange_rate=0.9698795181),
                          Transaction(date=datetime.date(2022, 12, 2),
                                      payer_or_payee='MATJAZ DROLC, S.P.',
                                      payer_or_payee_account_number='SI5601234567890',
                                      transaction_type='Income',
                                      payment_reference='Let it rain',
                                      amount_eur=100000,
                                      amount_foreign_currency=None,
                                      foreign_currency_type=None,
                                      exchange_rate=None)], Transaction.from_file(
            os.path.join(os.path.dirname(__file__), 'fixtures', 'test_n26.csv')))


if __name__ == '__main__':
    unittest.main()
