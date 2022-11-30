"""
class HTML
class HTMLObject
class Section
class FootNoteSection
class FootNote
class PreviewSection
class Table
class Div
"""

from ast import Index


def StrMatch(txt, pos, target):
	i = 0
	while i < len(target):
		try:
			if txt[pos+i] != target[i]: return False
		except IndexError:
			return False
		i += 1
	return True

class HTMLObject():
	def __init__(self):
		# 0: default text
		# 1: style
		# 2: block
		# 3: heading
		# 4: section
		self.type = 0
		self.txt  = ''
		self.head = ''

	def addtype(self, type):
		match type:
			case 'em':     self.type |= 1
			case 'strong': self.type |= 2
			case 'ins':    self.type |= 4
			case 'strike': self.type |= 8
			case 'code':   self.type |= 16
			case 'mark':   self.type |= 32
			case 'sup':    self.type |= 64
			case 'sub':    self.type |= 128
			case 'half':   self.type |= 256
	def remtype(self, type):
		match type:
			case 'em':     self.type &= ~1
			case 'strong': self.type &= ~2
			case 'ins':    self.type &= ~4
			case 'strike': self.type &= ~8
			case 'code':   self.type &= ~16
			case 'mark':   self.type &= ~32
			case 'sup':    self.type &= ~64
			case 'sub':    self.type &= ~128
			case 'half':   self.type &= ~256

		self.type & 0x1FF

	def push(self, data): self.txt += data
	def __len__(self): return len(self.txt)

	def __repr__(self):
		tags = []
		rets = ''
		rete = ''

		tags = ['em', 'strong', 'ins', 'strike',
			'code', 'mark', 'sup', 'sub', 'half']

		for i in range(9):
			if self.type & 2**i:
				rets += f"<{tags[i]}>"
				rete += f"</{tags[i]}>"

		return f"{rets}{self.txt}{rete}"


def Parse(path, format, autoopen=False):
	file = open(path)
	text = file.read(0xFFFF)
	ls   = [HTMLObject()]

	# style
	i = 0

	tab = 0

	em     = False
	strong = False
	ins    = False
	strike = False
	code   = False
	mark   = False
	sup    = False
	sub    = False
	half   = False

	head = 0

	while i < len(text):
		try:
			ch = text[i]
			chn = text[i+1]
			chp = text[i-1]

			if type(ls[-1]) is not HTMLObject: # if there is text
				ls.append(HTMLObject())
				try:
					ls[-1].type = ls[-2].type
				except AttributeError: pass

			if ch == '\t':
				tab += 1
				continue
			else: tab = 0

			if ch == '\n':
				if chn == '\n':
					ls[-1].push('<br>')
					i += 1
				else: ch = ' '

			if StrMatch(text, i, '---'):
				ls.append('<hr>')
				ls.append(HTMLObject())
				i += 3
				continue

			if head == 0 and (i == 0 or chp == '\n'):
				if StrMatch(text, i, '#.'):       head = 1
				elif StrMatch(text, i, '######'): head = 7
				elif StrMatch(text, i, '#####'):  head = 6
				elif StrMatch(text, i, '####'):   head = 5
				elif StrMatch(text, i, '###'):    head = 4
				elif StrMatch(text, i, '##'):     head = 3
				elif StrMatch(text, i, '#'):      head = 2

				if head != 0:
					ls.append(f"<{['hsmall','h1','h2','h3','h4','h5','h6'][head-1]}>")
					ls.append(HTMLObject())
					i += head if head != 1 else 3
					continue

			if head != 0 and text[i] == '\n':
				ls.append(f"</{['hsmall','h1','h2','h3','h4','h5','h6'][head-1]}>")
				ls.append(HTMLObject())
				head = 0

			# if there is not text, add your type
			# if there is text, make a new element and add your new type
			# if there is text and you are removing a type,
			# make a new element without your type
			if ch == '\\' or (ch == '¬' and code == True):
				pass

			if ch == '`':
				code ^= 1

				if len(ls[-1]):
					ls.append(HTMLObject())
					try: ls[-1].type = ls[-2].type
					except AttributeError: pass


				if code: ls[-1].addtype('code')
				else:    ls[-1].remtype('code')
			elif ch == '^':
				sup ^= 1

				if sup:  ls[-1].addtype('sup')
				else:    ls[-1].remtype('sup')
			elif ch == '*':
				if chn == '*':
					strong ^= 1

					if len(ls[-1]):
						ls.append(HTMLObject())
						try: ls[-1].type = ls[-2].type
						except AttributeError: pass


					if strong: ls[-1].addtype('strong')
					else:      ls[-1].remtype('strong')

					i += 1
				else:
					em ^= 1

					if len(ls[-1]):
						ls.append(HTMLObject())
						try: ls[-1].type = ls[-2].type
						except AttributeError: pass

					if em: ls[-1].addtype('em')
					else:  ls[-1].remtype('em')
			elif ch == '_':
				if chn == '_':
					ins ^= 1

					if len(ls[-1]):
						ls.append(HTMLObject())
						try: ls[-1].type = ls[-2].type
						except AttributeError: pass

					if ins: ls[-1].addtype('ins')
					else:   ls[-1].remtype('ins')

					i += 1
				else:
					sub ^= 1

					if len(ls[-1]):
						ls.append(HTMLObject())
						try: ls[-1].type = ls[-2].type
						except AttributeError: pass

					if sub: ls[-1].addtype('sub')
					else:   ls[-1].remtype('sub')
			elif ch == '=':
				if chn == '=':
					mark ^= 1

					if len(ls[-1]):
						ls.append(HTMLObject())
						try: ls[-1].type = ls[-2].type
						except AttributeError: pass

					if mark: ls[-1].addtype('mark')
					else:    ls[-1].remtype('mark')

					i += 1
				else:
					half ^= 1

					if len(ls[-1]):
						ls.append(HTMLObject())
						try: ls[-1].type = ls[-2].type
						except AttributeError: pass

					if half: ls[-1].addtype('half')
					else:    ls[-1].remtype('half')
			elif StrMatch(text, i, '~~'):
				strike ^= 1

				if len(ls[-1]):
						ls.append(HTMLObject())
						try: ls[-1].type = ls[-2].type
						except AttributeError: pass

				if strike: ls[-1].addtype('strike')
				else:      ls[-1].remtype('strike')

				i += 1
			else:
				ls[-1].push(ch)
		except IndexError:
			break
		i += 1

	return ls


def main(args):
	input = ''
	output = 'Output.mr'
	format = 0 # 0: HTML, 1: PDF, 2: SVG, 3: PNG, 4: EPUB
	stylesheet = None

	if len(args) < 2:
		print("MarkRight requieres at least 1 arguement\nUse -h if you need help")
	else:
		i = 1
		while i < len(args):
			if args[i][0] == '-':
				match args[i][1]:
					case 'h': Parse("./Syntax.me", format, True)
					case 'o':
						if i < len(args)-1:
							output = args[i+1]
							i += 1
						else: print("MarkRight requires one more arguements after '-o'")
					case 'f':
						if i < len(args)-1:
							if args[i+1] == "html":	  format = 0
							elif args[i+1] == "pdf":  format = 1
							elif args[i+1] == "svg":  format = 2
							elif args[i+1] == "png":  format = 3
							elif args[i+1] == "epub": format = 4
							else: print(f"Wrong format parameter on position {i+1}")
							i += 1
					case 's':
						if i < len(args)-1:
							stylesheet = args[i+1]
			else: input = args[i]

			i += 1

	print(f"{input}, {output}\n{format}, {stylesheet}")

	ls = Parse(input, format)

	# print(ls)

	o = open(output, 'w')
	for i in ls:
		o.write(str(i))

	return 0;



if __name__ == "__main__":
	from sys import argv
	main(argv)
