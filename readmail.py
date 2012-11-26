#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding('utf-8')
import sys
from pprint import pprint

import email_interface
import docs_interface
import tags # tags.tags = { u"name": ['nicknames', ...], ... }


import re

try:
	import * from local_settings.py
except:
	EMAIL = 'somemail@gmail.com'
	PASSWORD  = 'somepassword'
	SPREADSHEET = 'someuglylookinggooglespreadsheethash'
	DEBUG = True

email_interface.DEBUG = DEBUG

docs_interface.EMAIL    = email_interface.EMAIL    = EMAIL
docs_interface.PASSWORD = email_interface.PASSWORD = PASSWORD

docs_interface.SPREADSHEET = dict(
    key   = SPREADSHEET
    sheet = 'od6'
)


def detect_numbers(line):
	num1 = ur'(^|\s)([0-9]{3,})(\s|$)'
	num2 = ur'(^|\s)([0-9]{1,})\s*(тр|К|K|k|к|ТР)(\s|$)'
	m = re.search(num1, line)
	if not m:
		m = re.search(num2, line)
	if m:
		result = int(m.group(2))
		try:
			m.group(3)
		except:
			return result
		if m.group(3):
			if 'кkКK'.find(m.group(3)) >= 0 or len(m.group(3)) > 1:
				result *= 1000
		return result
	num3 = r'([0-9+]{5,})'
	m = re.search(num3, line)
	if m:
		results = [int(x) for x in m.group(1).split('+')]
		sum=0
		for i in results:
			sum+=i
		return sum
	return None #''

def is_report(lineset):
	if re.search(ur'Состояние', lineset[0]):
		return True
	if re.search(ur'Финплан', lineset[0]):
		return True
	if re.search(ur'Отчёт', lineset[0]):
		return True
	if re.search(ur'Отчет', lineset[0]):
		return True
	if re.search(ur'Инструкция', lineset[0]):
		return True
	return False


def checkout():
	for i in email_interface.iterate_gmail():
		for l in i['lines']:
			print '"%s",' % l



def test_detect_numbers():
	import debug_data
	print
	for i in debug_data.data:
		print '%s\t\t%s' % (str(detect_numbers(i)), i)
	print



# работа с тагами
def prepare_tags():
	taglist = []
	for t in tags.tags.items():
		taglist.append( (unicode(t[0]).lower(), t[0]) )
		for tt in t[1]:
			taglist.append( (unicode(tt).lower(), t[0]) )
	return taglist

def prepare_tags_regex(taglist):
	r = []
	for tag, name in taglist:
		r.append( '('+tag+')' )
	return ur'(\s)' + '|'.join(r) + '\s'

def find_tag(taglist, tagre, line):
	m = re.search(tagre, unicode(' '+line+' ').lower())
	if m:
		i = m.lastindex-2
		tag, name = taglist[i]
		return name
	return ''# None


def test_detect_tags():
	import debug_data
	t = prepare_tags()
	tre = prepare_tags_regex(t)
	print tre
	print
	for i in debug_data.data:
		print '%s\t\t%s' % (str(find_tag(t, tre, i)), i)
	print



# готовимся к выводу
def comment(item, line=None):
	r = []
	if line and item['lines'][0] != line:
		r = [line, ' == ']
	r.append( '; '.join(item['lines']) )
	return "".join(r)


def proceed_iterator():
	tags = prepare_tags()
	tags_regex = prepare_tags_regex(tags)

	for i in email_interface.iterate_gmail():
		# получили письмо, и если оно не по шаблону отчёта, то обрабатываем
		if not is_report(i['lines']):
			is_processed = False
			tag = ' '
			for l in i['lines']:
				# каждую строчку отдельно: ищем сумму и таг
				# если сумма не нулевая, то мы заносим её в общий реестр
				amount = detect_numbers(l)
				new_tag = find_tag(tags, tags_regex, l)
				if tag == ' ' and new_tag is not None:
					tag = new_tag
				if amount is not None:
					is_processed = True
					yield dict(
						datetime= i['date'], #.strftime('%d.%m.%y')
						tag= tag,
						amount = amount, 
						comments = comment(i, l)
						)
			# если ни одной суммы в письме не нашли, то заносим её в дополнительный реестр
			if not is_processed:
				yield dict(
					datetime = i['date'],
					tag='', amount='',
					comments = comment(i)
					)

def main():
	for line in proceed_iterator():
		line['month'] = line['datetime'].strftime('%Y-%m')
		line['date']  = line['datetime'].strftime('%Y-%m-%d')
		del line['datetime']
		# print line['date'], line['tag'], '\t', line['amount'], '\t', line['comments']
		docs_interface.push(line)


main()
# test_detect_numbers()
# test_detect_tags()
