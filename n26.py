import csv
import datetime
from dataclasses import dataclass
from decimal import Decimal
from io import TextIOBase
from typing import Optional, List


def _str_or_none(s: str) -> Optional[str]:
    """Return the string; or None for empty strings"""
    return s if len(s) > 0 and s != "-" else None


def _parse_amount(s: str) -> Optional[Decimal]:
    """Parse an amount (i.e. 11353.15) into a Decimal"""
    if len(s) == 0:
        return None

    return Decimal(s)


@dataclass
class Transaction:
    """N26 transaction"""

    date: datetime.date
    """Transaction date"""

    payer_or_payee: str
    """The payer or payee"""

    payer_or_payee_account_number: Optional[str]
    """The payer or payee Account number"""

    transaction_type: str
    """Transaction type, i.e. 'MoneyBeam', 'Income', or 'MasterCard Payment'"""

    payment_reference: Optional[str]
    """Reference or description"""

    amount_eur: Decimal
    """The amount in EURO cents"""

    amount_foreign_currency: Optional[Decimal]
    """The amount in foreign currency"""

    foreign_currency_type: Optional[str]
    """Foreign currency type, i.e. 'EUR' or 'USD'.
    
    Note: some EUR payments will have this set to 'EUR', instead of blank.
    """

    exchange_rate: Optional[Decimal]
    """The exchange rate between EUR and the foreign currency.
    
    If foreign currency is EUR, this is 1.0"""

    @classmethod
    def from_text(cls, text: TextIOBase) -> List['Transaction']:
        reader = csv.reader(text, delimiter=",", quoting=csv.QUOTE_ALL, quotechar='"')

        assert next(reader) == ["Date", "Payee", "Account number", "Transaction type", "Payment reference",
                                "Amount (EUR)", "Amount (Foreign Currency)", "Type Foreign Currency", "Exchange Rate"]

        return [
            Transaction(
                date=datetime.date.fromisoformat(t[0]),
                payer_or_payee=t[1],
                payer_or_payee_account_number=_str_or_none(t[2]),
                transaction_type=t[3],
                payment_reference=_str_or_none(t[4]),
                amount_eur=_parse_amount(t[5]),
                amount_foreign_currency=_parse_amount(t[6]),
                foreign_currency_type=_str_or_none(t[7]),
                exchange_rate=Decimal(t[8]) if len(t[8]) > 0 else None

            ) for t in reader
        ]

    @classmethod
    def from_file(cls, filename: str) -> List['Transaction']:
        with open(filename, 'rt', encoding='utf8') as f:
            return cls.from_text(f)
