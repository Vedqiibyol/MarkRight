#!/usr/bin/python

import re
import os

comment  = '\x1B[0m\x1B[2m';  reComment = re.compile(r'^(#.+$)')
string   = '\x1B[0m\x1B[33m'; reString  = re.compile(r'^(\'.*\'|".*")') # (\'{3}.+\'{3})|("{3}.+"{3})|
keyword  = '\x1B[0m\x1B[35m'; reKeyword = re.compile(r'^(if|elif|else|try|except|import|from|as|in|for|while)')
op       = '\x1B[0m\x1B[34m'; reOp      = re.compile(r'^([:\+\-\*/%\=<>!@^&~]|->)')
type     = '\x1B[0m\x1B[31m'; reType    = re.compile(r'^(def|class|lambda|int|float|str|object|list|dict|tuple|0x|0b|0o)')
num      = '\x1B[0m\x1B[32m'; reNum     = re.compile(r'^(-?x[\dabcdef_]+|-?[\d_]+|-?o[01234567_]+|-?b[01_]+)')
punct    = '\x1B[0m\x1B[36m'; rePunct   = re.compile(r'^([\(\)\[\]{};])')
function = '\x1B[0m\x1B[38;2;255;128;0m'; reFunction = re.compile(r'^(\w+)\(')
escape   = '\x1B[0m\x1B[38;2;215;200;0m'; reEscape   = re.compile(r'^(\\(x[\da-fA-F]{2}\[?|u[\da-fA-F]{4}\[?|[abfknrstvz]))')
nothing  = '\x1B[0m'

def Print(*args):
	print(*args, sep='', end='')

def main(args):
	f = None
	try:
		if os.path.isfile(args[1]):
			f = open(args[1])

			ln = f.readline()

			flags = {
				'comment': False, 'string':   False,
				'keyword': False, 'op':       False,
				'type':    False, 'num':      False,
				'punct':   False, 'function': False,
				'escape':  False, 'nothing':  False
			}

			while ln:
				i = 0
				while i <= len(ln):
					if (m := reComment.match(ln[i:])):
						flags['comment'] = True
						Print(comment)
					elif (m := reString.match(ln[i:])) and not flags['comment']:
						flags['string'] = True
						Print(string)
					elif (m := reType.match(ln[i:])) and not (flags['comment'] or flags['string']):
						flags['type'] = True
						Print(keyword)
					elif (m := reKeyword.match(ln[i:])) and not (flags['comment'] or flags['string']):
						flags['keyword'] = True
						Print(keyword)
					elif (m := reOp.match(ln[i:])) and not (flags['comment'] or flags['string']):
						flags['op'] = True
						Print(op)
					elif (m := reNum.match(ln[i:])) and not (flags['comment'] or flags['string']):
						flags['num'] = True
						Print(keyword)
					elif (m := reEscape.match(ln[i:])) and flags['string']:
						Print(escape, m.group(1), string)

					Print(ln[i])
					i += 1

				ln = f.readline()
				flags['comment'] = False
				print()
		else:
			print('not a file')
			exit(-1)
	except IndexError:
		print('\x1B[31mrequires one argument\x1B[0m')

if __name__ == '__main__':
	import sys
	# from colorama import init
	# init()
	main(sys.argv)