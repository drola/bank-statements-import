#!/usr/bin/env python3
import datetime
import xml.etree.ElementTree as ET

from ofxtools.header import make_header
from ofxtools.models import *

from delavska_hranilnica import TransactionExport


def dh2ofx(dh: TransactionExport) -> str:
    message = ""
    status = STATUS(code=0, severity='INFO')

    acctfrom = BANKACCTFROM(bankid='', acctid=dh.account.account_number, accttype='CHECKING')
    ledgerbal = LEDGERBAL(balamt=Decimal('150.00'), dtasof=datetime.datetime(tzinfo=datetime.timezone.utc))

    # TODO: Put together list of STMTTRN (transactions). Spec page 215
    banktranlist = BANKTRANLIST()  # TODO, Spec page 208
    stmtrs = STMTRS(curdef='EUR', bankacctfrom=acctfrom, banktranlist=banktranlist)
    stmttrnrs = STMTTRNRS(trnuid='0', status=status, stmtrs=stmtrs)
    bankmsgsrs = BANKMSGSRSV1(stmttrnrs)
    sonrs = SONRS(
        status=status,
        dtserver=datetime.datetime.now(datetime.timezone.utc),
        language='ENG',
        fi=FI(org=dh.account.bank)
    )
    signonmsgs = SIGNONMSGSRSV1(sonrs=sonrs)
    ofx = OFX(signonmsgsrsv1=signonmsgs, bankmsgsrsv1=bankmsgsrs)

    root = ofx.to_etree()
    message = ET.tostring(root).decode()
    header = str(make_header(version=220))
    return header + message
