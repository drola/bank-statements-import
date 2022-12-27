import datetime
import os
from decimal import Decimal

from delavska_hranilnica import TransactionsExport, Transaction as DHTransaction, Account
from n26 import Transaction as N26Transaction

delavska_hranilnica_transactions_export = TransactionsExport(account=Account(bank='DELAVSKA HRANILNICA D.D. LJUBLJANA',
                                                                             owner='JANEZ KRANJSKI',
                                                                             account_number='SI56 6100 0001 0000 001'),
                                                             export_from=datetime.date(2022, 9, 28),
                                                             export_to=datetime.date(2022, 12, 24),
                                                             export_date=datetime.date(2022, 12, 24),
                                                             final_balance=Decimal('20050.00'),
                                                             transactions=[DHTransaction(currency='EUR',
                                                                                         value_date=datetime.date(2022,
                                                                                                                  12,
                                                                                                                  13),
                                                                                         posting_date=datetime.date(
                                                                                             2022,
                                                                                             12,
                                                                                             13),
                                                                                         transaction_id='123456520',
                                                                                         reclamation_nr='860000123456520',
                                                                                         payer_or_payee='DELAVSKA '
                                                                                                        'HRANILNICA d.d. '
                                                                                                        'LJUBLJANA',
                                                                                         amount_paid=Decimal('100.00'),
                                                                                         amount_received=None,
                                                                                         reference_payee='SI99',
                                                                                         reference_payer='SI99',
                                                                                         description='PRILIVNA PROVIZIJA'),
                                                                           DHTransaction(currency='EUR',
                                                                                         value_date=datetime.date(2022,
                                                                                                                  12,
                                                                                                                  13),
                                                                                         posting_date=datetime.date(
                                                                                             2022,
                                                                                             12,
                                                                                             13),
                                                                                         transaction_id='123456519',
                                                                                         reclamation_nr='860000123456519',
                                                                                         payer_or_payee='PayPal',
                                                                                         amount_paid=None,
                                                                                         amount_received=Decimal(
                                                                                             '150.00'),
                                                                                         reference_payee='SI99',
                                                                                         reference_payer='123123123',
                                                                                         description='San Francisco, CA')])

test_delavska_hranilnica_csv = os.path.join(os.path.dirname(__file__), 'test_delavska_hranilnica.csv')

n26_transactions = [N26Transaction(date=datetime.date(2022, 1, 12),
                                   payer_or_payee='SPOTIFY',
                                   payer_or_payee_account_number=None,
                                   transaction_type='MasterCard Payment',
                                   payment_reference=None,
                                   amount_eur=Decimal('-5.99'),
                                   amount_foreign_currency=Decimal('-5.99'),
                                   foreign_currency_type='EUR',
                                   exchange_rate=Decimal('1.0')),
                    N26Transaction(date=datetime.date(2022, 10, 4),
                                   payer_or_payee='Johnny',
                                   payer_or_payee_account_number='IT1234567890',
                                   transaction_type='MoneyBeam',
                                   payment_reference='The gift',
                                   amount_eur=Decimal('-20.00'),
                                   amount_foreign_currency=None,
                                   foreign_currency_type=None,
                                   exchange_rate=None),
                    N26Transaction(date=datetime.date(2022, 12, 1),
                                   payer_or_payee='DIGITALOCEAN.COM',
                                   payer_or_payee_account_number=None,
                                   transaction_type='MasterCard Payment',
                                   payment_reference=None,
                                   amount_eur=Decimal('-1.61'),
                                   amount_foreign_currency=Decimal('-1.66'),
                                   foreign_currency_type='USD',
                                   exchange_rate=Decimal('0.9698795181')),
                    N26Transaction(date=datetime.date(2022, 12, 2),
                                   payer_or_payee='MATJAZ DROLC, S.P.',
                                   payer_or_payee_account_number='SI5601234567890',
                                   transaction_type='Income',
                                   payment_reference='Let it rain',
                                   amount_eur=Decimal('1000.00'),
                                   amount_foreign_currency=None,
                                   foreign_currency_type=None,
                                   exchange_rate=None)]
test_n26_csv = os.path.join(os.path.dirname(__file__), 'test_n26.csv')

test_dh2ofx_ofx = os.path.join(os.path.dirname(__file__), 'test_dh2ofx.ofx')
