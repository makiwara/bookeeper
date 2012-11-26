#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding('utf-8')
import sys; 
sys.path.insert(1, "../")

import time
import gdata.spreadsheet.service
from pprint import pprint


EMAIL = 'email@gmail.com'
PASSWORD = 'pwd'


SPREADSHEET = dict(
    key   = 'gdocs_key',
    sheet = 'od6' # usually it is
)


def push(line, sheet=None):
    if sheet is None:
        sheet = SPREADSHEET['sheet']
    spr_client = gdata.spreadsheet.service.SpreadsheetsService()
    spr_client.email = EMAIL
    spr_client.password = PASSWORD
    spr_client.source = 'Humanemagica Butler'
    spr_client.ProgrammaticLogin()

    line['amount'] = unicode(line['amount'])

    entry = spr_client.InsertRow(line, SPREADSHEET['key'], sheet)
    if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
      print 'OK ', line['date'], line['amount'], line['tag'], '==', line['comments']
    else:
      print 'Err', line['date'], line['amount'], line['tag'], '==', line['comments']



DEBUG_LINE = dict(
    month='2012-09',
    date='2012-09-23',
    amount='1000.00',
    tag='подарки',
    comments='подарки на день рождения Коли'
)

#push(DEBUG_LINE)
