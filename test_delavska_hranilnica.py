import datetime
import os.path
import unittest

from delavska_hranilnica import _parse_date, _parse_amount, TransactionExport, Transaction, Account


class DelavskaHranilnicaTestCase(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(datetime.date(2021, 12, 23), _parse_date("23.12.2021"))

        with self.assertRaises(ValueError):
            _parse_date("unexpected")

    def test_parse_amount(self):
        self.assertEqual(1234567, _parse_amount('12.345,67'))
        self.assertEqual(1234500, _parse_amount('12345'))
        self.assertEqual(1234560, _parse_amount('12345,6'))
        self.assertEqual(None, _parse_amount(''))

        with self.assertRaises(AssertionError):
            _parse_amount('12345,678')

    def test_from_file(self):
        self.assertEqual(TransactionExport(account=Account(bank='DELAVSKA HRANILNICA D.D. LJUBLJANA',
                                                           owner='JANEZ KRANJSKI',
                                                           account_number='SI56 6100 0001 0000 001'),
                                           export_from=datetime.date(2022, 9, 28),
                                           export_to=datetime.date(2022, 12, 24),
                                           export_date=datetime.date(2022, 12, 24),
                                           transactions=[Transaction(currency='EUR',
                                                                     value_date=datetime.date(2022, 12, 13),
                                                                     posting_date=datetime.date(2022, 12, 13),
                                                                     transaction_id='123456520',
                                                                     reclamation_nr='860000123456520',
                                                                     payer_or_payee='DELAVSKA '
                                                                                    'HRANILNICA d.d. '
                                                                                    'LJUBLJANA',
                                                                     amount_paid=10000,
                                                                     amount_received=None,
                                                                     reference_payee='SI99',
                                                                     reference_payer='SI99',
                                                                     description='PRILIVNA PROVIZIJA'),
                                                         Transaction(currency='EUR',
                                                                     value_date=datetime.date(2022, 12, 13),
                                                                     posting_date=datetime.date(2022, 12, 13),
                                                                     transaction_id='123456519',
                                                                     reclamation_nr='860000123456519',
                                                                     payer_or_payee='PayPal',
                                                                     amount_paid=None,
                                                                     amount_received=15000,
                                                                     reference_payee='SI99',
                                                                     reference_payer='123123123',
                                                                     description='San Francisco, CA')]),
                         TransactionExport.from_file(
                             os.path.join(os.path.dirname(__file__), 'fixtures', 'test_delavska_hranilnica.csv')))


if __name__ == '__main__':
    unittest.main()
