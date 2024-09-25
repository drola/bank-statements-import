#!/usr/bin/env python3
import argparse
import datetime
import hashlib
import os.path
import warnings
import xml.etree.ElementTree as ET
from decimal import Decimal
from typing import List

from ofxtools.Types import OFXTypeWarning
from ofxtools.header import make_header
from ofxtools.models import *

from n26_legacy import Transaction


def recognize_trntype(t: Transaction) -> str:
    """Determine transaction type.

    See OFX spec, section 11.4.4.3
    """

    # For now, we only use CREDIT (generic credit) and DEBIT (generic debit)
    # There are more interesting types:
    # INT=interest rate earned/paid
    # FEE=FI fee
    # SRVCHG=Service charge
    # DEP=deposit
    # ATM=ATM debit/credit
    # POS=point of sale debit/credit
    # XFER=transfer
    # PAYMENT=electronic payment
    # CASH=cash withdrawal;
    # It would be possible to infer some of them based on transaction description
    return 'CREDIT' if t.amount_eur < 0 else 'DEBIT'


def date2datetime(d: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(d, datetime.time(tzinfo=datetime.timezone.utc), tzinfo=datetime.timezone.utc)


def calculate_fitid(t: Transaction) -> str:
    s = f"{t.date.isoformat()}{t.amount_eur}{t.payer_or_payee}{t.payment_reference}"
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def transaction2stmttrn(t: Transaction) -> STMTTRN:
    """Construct a transaction entry.

    See section 11.4.4.1 in the OFX spec."""
    with warnings.catch_warnings():
        # Supress warning for too long string
        # Typically happens with <NAME> field on transactions
        warnings.filterwarnings('ignore', message='NagString', category=OFXTypeWarning)
        return STMTTRN(
            trntype=recognize_trntype(t),
            dtposted=date2datetime(t.date),
            trnamt=t.amount_eur,
            fitid=calculate_fitid(t),
            name=t.payer_or_payee,
            memo=t.payment_reference
        )


def n262ofx(transactions: List[Transaction], account_number: str) -> str:
    status = STATUS(code=0, severity='INFO')

    # For accid, we remove spaces to get within the 22-character length limit
    acctfrom = BANKACCTFROM(bankid='NTSBDEB1', acctid=account_number.replace(' ', ''), accttype='CHECKING')
    ledgerbal = LEDGERBAL(balamt=Decimal(0.0),
                          dtasof=datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc))

    # OFX Spec, 11.4.4
    banktranlist = BANKTRANLIST(
        *[transaction2stmttrn(t) for t in transactions],
        dtstart=date2datetime(min([t.date for t in transactions])),
        dtend=date2datetime(max(t.date for t in transactions)),
    )
    # OFX Spec, 11.4.2.2
    stmtrs = STMTRS(curdef='EUR', bankacctfrom=acctfrom, banktranlist=banktranlist, ledgerbal=ledgerbal)
    stmttrnrs = STMTTRNRS(trnuid='0', status=status, stmtrs=stmtrs)
    bankmsgsrs = BANKMSGSRSV1(stmttrnrs)
    sonrs = SONRS(
        status=status,
        dtserver=datetime.datetime.now(datetime.timezone.utc),
        language='ENG',
        fi=FI(org='N26 BANK GMBH'))
    signonmsgs = SIGNONMSGSRSV1(sonrs=sonrs)
    ofx_ = OFX(signonmsgsrsv1=signonmsgs, bankmsgsrsv1=bankmsgsrs)

    with warnings.catch_warnings():
        # Supress warning for too long string
        # Typically happens with <NAME> field on transactions
        warnings.filterwarnings('ignore', message='NagString', category=OFXTypeWarning)
        root = ofx_.to_etree()
    message = ET.tostring(root).decode()
    header = str(make_header(version=220))
    return (header + message).replace("\r\n", "")


def main():
    parser = argparse.ArgumentParser(description='Convert transactions in CSV from N26 GMBH to OFX files.')
    parser.add_argument('--account-number', required=True, help='Account number')
    parser.add_argument('csv_files', nargs='+', help='CSV files',
                        type=argparse.FileType('rt', encoding='utf-8'))
    args = parser.parse_args()

    for f in args.csv_files:
        te = Transaction.from_text(f)
        result = n262ofx(te, args.account_number)
        if f.name == '<stdin>':
            print(result)
        else:
            out = f"{os.path.splitext(f.name)[0]}.ofx"
            with open(out, 'wt', encoding='utf-8') as of:
                of.write(result)


if __name__ == '__main__':
    main()
