#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding('utf-8')
import sys
from pprint import pprint


EMAIL = 'email@gmail.com'
PASSWORD = 'pwd'

DEBUG = False


from email.Header import decode_header
import gmail
from datetime import datetime


def decode(line):
    decoded, encoding = decode_header(line)[0]
    if encoding:
        return decoded.decode(encoding)
    else:
        return decoded

def decode_date(date):
    months = dict( Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12 )
    p1 = date.split(", ")
    p2 = p1[1].split(" ")
    d = int(p2[0])
    m = months[p2[1]]
    y = int(p2[2])
    return datetime(y, m, d)

def iterate_gmail():
    conn = gmail.Gmail(EMAIL, PASSWORD)
    msgs = conn.search.unread().all()
    for msg in msgs:
        subject = decode(msg.subject())
        if DEBUG:
            msg.unread() 
        date = decode_date(msg.message["Date"])
        body = msg.message.get_payload(decode=True)
        lines = [subject]
        if isinstance(body, list):
            body = body[0].get_payload()
        if body:
            body = body.decode('koi8-r')
            more_lines = body.split('\n')
            lines = lines + more_lines
        new_lines = []
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                new_lines.append(line)
        yield dict(
            date= date,
            lines= new_lines
        )
    conn.logout()

