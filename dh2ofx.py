#!/usr/bin/env python3
import argparse
import datetime
import os.path
import warnings
import xml.etree.ElementTree as ET
from decimal import Decimal

from ofxtools.Types import OFXTypeWarning
from ofxtools.header import make_header
from ofxtools.models import *

from delavska_hranilnica import TransactionsExport, Transaction


def transaction_amount(t: Transaction) -> Decimal:
    if t.amount_paid is not None:
        return t.amount_paid.copy_negate()
    else:
        return t.amount_received


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
    return 'CREDIT' if t.amount_paid is not None else 'DEBIT'


def date2datetime(d: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(d, datetime.time(tzinfo=datetime.timezone.utc), tzinfo=datetime.timezone.utc)


def transaction2stmttrn(t: Transaction) -> STMTTRN:
    """Construct a transaction entry.

    See section 11.4.4.1 in the OFX spec."""
    with warnings.catch_warnings():
        # Supress warning for too long string
        # Typically happens with <NAME> field on transactions
        warnings.filterwarnings('ignore', message='NagString', category=OFXTypeWarning)
        return STMTTRN(
            trntype=recognize_trntype(t),
            dtposted=date2datetime(t.posting_date),
            dtavail=date2datetime(t.value_date),
            trnamt=transaction_amount(t),
            fitid=t.reclamation_nr,  # Because t.transaction_id is sometimes empty
            name=t.payer_or_payee,
            memo=t.description,
            refnum=t.reference_payee
        )


def dh2ofx(dh: TransactionsExport) -> str:
    status = STATUS(code=0, severity='INFO')

    # For accid, we remove spaces to get within the 22-character length limit
    acctfrom = BANKACCTFROM(bankid='HDELSI22', acctid=dh.account.account_number.replace(' ', ''), accttype='CHECKING')
    ledgerbal = LEDGERBAL(balamt=dh.final_balance, dtasof=date2datetime(dh.export_to))

    # OFX Spec, 11.4.4
    banktranlist = BANKTRANLIST(
        *[transaction2stmttrn(t) for t in dh.transactions],
        dtstart=date2datetime(dh.export_from),
        dtend=date2datetime(dh.export_to),
    )
    # OFX Spec, 11.4.2.2
    stmtrs = STMTRS(curdef='EUR', bankacctfrom=acctfrom, banktranlist=banktranlist, ledgerbal=ledgerbal)
    stmttrnrs = STMTTRNRS(trnuid='0', status=status, stmtrs=stmtrs)
    bankmsgsrs = BANKMSGSRSV1(stmttrnrs)
    sonrs = SONRS(
        status=status,
        dtserver=datetime.datetime.now(datetime.timezone.utc),
        language='ENG',
        fi=FI(org=dh.account.bank.replace('LJUBLJANA', '').strip())
        # Removing "LJUBLJANA" to get within 32-character limit
    )
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
    parser = argparse.ArgumentParser(description='Convert transactions in CSV from Delavska Hranilnica to OFX files.')
    parser.add_argument('csv_files', nargs='+', help='CSV files',
                        type=argparse.FileType('r'))
    args = parser.parse_args()

    for f in args.csv_files:
        f.reconfigure(encoding='cp1250')
        te = TransactionsExport.from_text(f)
        result = dh2ofx(te)
        if f.name == '<stdin>':
            print(result)
        else:
            out = f"{os.path.splitext(f.name)[0]}.ofx"
            with open(out, 'wt', encoding='utf-8') as of:
                of.write(result)


if __name__ == '__main__':
    main()
