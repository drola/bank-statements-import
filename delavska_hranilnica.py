import csv
import datetime
from dataclasses import dataclass
from decimal import Decimal
from io import TextIOBase
from typing import List, Optional


def _parse_date(d: str) -> datetime.date:
    """Parse a date in DD.MM.YYYY format (i.e. 13.12.2022)"""
    return datetime.datetime.strptime(d, "%d.%m.%Y").date()


def _parse_amount(a: str) -> Optional[Decimal]:
    """Parse an amount (i.e. 11.353,15) into a Decimal"""
    if len(a) == 0:
        return None

    whole_and_fraction = a.replace('.', '').replace(',', '.')
    return Decimal(whole_and_fraction)


@dataclass
class Account:
    """Bank account info"""

    bank: str
    """Bank name"""

    owner: str
    """Account owner"""

    account_number: str
    """Account number"""


@dataclass
class Transaction:
    """Transaction details"""

    currency: str
    """3-letter currency code, i.e. 'EUR'"""

    value_date: datetime.date
    """The date when transaction took place (SLO: datum valute)"""

    posting_date: datetime.date
    """The date when transaction was processed (SLO: datum knjiženja)"""

    transaction_id: str
    """Bank's transaction ID"""

    reclamation_nr: str
    """Transaction number for reclamation purposes"""

    payer_or_payee: str
    """The other party in the transaction"""

    amount_paid: Optional[Decimal]
    """Amount paid, in cents"""

    amount_received: Optional[Decimal]
    """Amount received, in cents"""

    reference_payee: str
    """Payee's reference"""

    reference_payer: str
    """Payer's reference"""

    description: str
    """The description"""


@dataclass
class TransactionsExport:
    """Transaction export and metadata"""

    account: Account
    """Account info"""

    export_from: datetime.date
    """Export start date"""

    export_to: datetime.date
    """Export end date"""

    export_date: datetime.date
    """The date of the export"""

    final_balance: Decimal

    transactions: List[Transaction]
    """Transactions"""

    @classmethod
    def from_text(cls, text: TextIOBase) -> 'TransactionsExport':
        reader = csv.reader(text, delimiter=';', )

        bank_line = next(reader)
        assert bank_line[0] == 'Banka:'
        bank = bank_line[1]
        owner_line = next(reader)
        assert owner_line[0] == 'Komitent:'
        owner = owner_line[1]

        from_and_to_dates_line = next(reader)
        assert from_and_to_dates_line[0] == 'Promet za obdobje:'
        from_and_to_dates = from_and_to_dates_line[1].split(' - ')
        export_from = _parse_date(from_and_to_dates[0])
        export_to = _parse_date(from_and_to_dates[1])

        export_date_line = next(reader)
        assert export_date_line[0] == 'Datum izpisa:'
        export_date = _parse_date(export_date_line[1])

        next(reader)  # empty line
        account_number_line = next(reader)
        assert account_number_line[0] == 'Račun'
        account_number = account_number_line[1]

        balances_header_line = next(reader)[0:5]
        assert balances_header_line == ['Valuta', 'Začetno stanje', 'Breme', 'Dobro', 'Končno stanje']
        [currency, initial_balance, total_paid, total_received, final_balance] = next(reader)[0:5]
        assert len(currency) == 3
        next(reader)

        account = Account(
            bank=bank,
            owner=owner,
            account_number=account_number
        )

        header_line = next(reader)
        assert header_line == ['Valuta', 'Datum valute', 'Datum knjiženja', 'ID transakcije',
                               'Št. za reklamacijo', 'Prejemnik / Plačnik', 'Breme', 'Dobro', 'Referenca plačnika',
                               'Referenca prejemnika', 'Opis prejemnika']

        # The following lines are transactions
        transactions = [cls._list_to_transaction(t) for t in reader if len(t) == len(header_line)]

        return cls(
            account=account,
            export_from=export_from,
            export_to=export_to,
            export_date=export_date,
            final_balance=_parse_amount(final_balance),
            transactions=transactions
        )

    @classmethod
    def from_file(cls, filename: str) -> 'TransactionsExport':
        with open(filename, 'rt', encoding='cp1250') as f:
            return cls.from_text(f)

    @classmethod
    def _list_to_transaction(cls, t: List) -> Transaction:
        return Transaction(
            currency=t[0],
            value_date=_parse_date(t[1]),
            posting_date=_parse_date(t[2]),
            transaction_id=t[3],
            reclamation_nr=t[4],
            payer_or_payee=t[5],
            amount_paid=_parse_amount(t[6]),
            amount_received=_parse_amount(t[7]),
            reference_payer=t[8],
            reference_payee=t[9],
            description=t[10]
        )
