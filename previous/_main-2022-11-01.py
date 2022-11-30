_reserved = " \t\n\r\"!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
_tab      = '\t' # FEKKIN F-STRING RULEZ!!!
_ln       = '\n'
_cnNull   = '\x1B[0m'
_cnRed    = '\x1B[41m'
_cnBlue   = '\x1B[44m'

# def strmatch(txt, pos, target): return txt[pos:][:len(target)] == target

def AddStyle(name: str, styles: dict) -> str:
	styles[name] ^= 1

	#ls[-1] += f"<{'/' * styles[style]}{style}>"

	return f"<{'/' * (not styles[name])}{name}>"

def GetValid(data) -> str:
	head = 0

	for i in data:
		if i not in _reserved:
			break
		head += 1

	tail = head

	for i in data[head:]:
		if i in _reserved:
			break
		tail += 1

	return data[head:tail]

def StripWhiteSpaces(data) -> tuple[str, int, int, int]:
	inc   = 0
	tab   = 0
	space = 0

	for i in data:
		if   i == '\t':   tab    += 1
		elif i == ' ' :   space  += 1
		elif i == '\r':   pass
		else: break

		inc += 1

	data  = data[inc:]
	after = len(data)

	data.rstrip()

	return (data, tab, space, after-len(data))


def IsTL(data) -> int:
	if data[:2] == '- ' or data[:2] == '-\t':
		if data[2:5][0] == '[' and data[2:5][0] == ']':
			if data[3] == ' ': return 0
			if data[3] == '-': return 1
			if data[3] == 'x': return 2
	return -1
def IsUL(data) -> bool:
	return data[:2] == '- ' or data[:2] == '-\t'
# TODO: add starting
def IsOL(data) -> tuple[bool, int]:
	cn = 0

	for i in data:
		if i == '.' and cn:
			break
		elif not i.isdigit():
			return [False, -1]

		cn += 1

	return [True, cn+1]

# def IsRL(data) -> tuple[bool, int]:

def LsEnding(index, tabs=0) -> str:
	tabh = tabs
	tabe = tabs + 1

	try:
		return [
			f"{_tab * tabe}</li>\n{_tab * tabh}</ul>",
			f"{_tab * tabe}</li>\n{_tab * tabh}</ol>",
			f"{_tab * tabe}</label>\n{_tab * tabh}</fieldset>",
			f"{_tab * tabe}</li>\n{_tab * tabh}</ol>"][index]
	except IndexError:
		return ''

def LsStart(index, tabs) -> str:
	try:
		return [
			_ln + f"{_tab * tabs}<ul>" + _ln,
			_ln + f"{_tab * tabs}<ol>" + _ln,
			_ln + f"{_tab * tabs}<fieldset class='task-list'>" + _ln,
			_ln + f"{_tab * tabs}<ol class='ref-list'>" + _ln][index]
	except IndexError:
		return ''

def LsClose(index, tabs) -> str:
	tabs += 1
	try:
		return [
			_ln + f"{_tab * tabs}</li>" + _ln,
			_ln + f"{_tab * tabs}</li>" + _ln,
			_ln + f"{_tab * tabs}</label>" + _ln,
			_ln + f"{_tab * tabs}</li>" + _ln][index]
	except IndexError:
		return ''

# TODO: add params
def LsAddHeader(ls: list, type: int, tabs: int) -> str:
	html = f'{_tab * (tabs+1)}</li>{_ln}'

	if len(ls):
		if ls[-1][1] > tabs:
			p    = ls.pop(-1)
			html = LsEnding(p[0])
		elif ls[-1][1] < tabs:
			last = ls[-1]
			ls.append([type, tabs])
			html += LsStart(type, tabs)
		elif ls[-1][0] != type:
			p     = ls.pop(-1)
			html  = LsEnding(p[0])
			ls.append([type, tabs])
			html += LsStart(type, tabs)
	else: # empty list, WTF?
		ls.append([type, tabs])
		html = LsStart(type, tabs)

	# TODO: task list with a new function
	# global value for each label
	# function `AddTLTag()`
	return html + f"{_tab * (tabs+1)}<li>{_ln}{_tab * (tabs+1)}"

def Parse(input):
	file = open(input)
	text = file.readline()
	html = ''

	# * Increment
	# You know what this is, so just don't touch it.
	# Thank you very much~
	i = 0

	# * Styling
	# The name of the tags are here as boolean.
	# When false the ``ParseStyle`` function should return a starting
	# HTML tag corresponding to the style examined by the function, and
	# toggle it's paired-value in the dictionary, making it ``True``;
	# when true, the ``ParseStyle`` function should return an ending
	# HTML tag [...] and set the value back to false.
	styles = {
		'em'     : False,
		'strong' : False,
		'ins'    : False,
		'strike' : False,
		'code'   : False,
		'mark'   : False,
		'sup'    : False,
		'sub'    : False,
		'half'   : False
	}

	head  = ''    # only one per line
	lists = []    # not that if non-empty, no <br> should be added
	depth = []    # current list depth
	newls = False # new list
	quote = 0
	codeb = None
	code  = False

	allows1 = True # allow lists, blockquotes, headings, separators to be written.
	               # False when text is encountered



	while text:
		data, tabs, spaces, after = StripWhiteSpaces(text)

		i  = 0
		j = 0

		try:
			# * Line breaks
			# TODO: make it with <p>
			# TODO: clean up
			if len(data) <= 1:
				if tabs == 0 and newls:
					while len(lists):
						html += LsEnding(lists.pop(-1)[0])
				elif not len(lists) and not codeb:
					html += '<br>'

			while i < len(data): # ``while len(text)``

				# later:
				# * Inline HTML styling

				# * Code block
				if   data[i:][:3] == '```':
					if codeb == None:
						i += 3
						codeb = GetValid(data[3:].strip())

						# TODO: TinyMCE
						html += f"<textarea class='codeblock' data-lang='{code}'>\n"

						allows1 = False
					else:
						codeb    = None
						allows1  = False
				elif data[i:][:2] == '``':
					code    ^= 1
					html    += '<' + ('/'*(not code)) + 'code>'
					i       += 2
					allows1  = False

				if not code or not codeb:
					# * Blockquotes
					if   data[i:][:2] == '<<':
						quote += 1
						html  += '<blockquote>\n'
						i     += 2
					elif data[i:][:2] == '>>' and quote:
						quote -= 1
						html  += '\n</blockquote>\n'
						i     += 2

					# * Lists, on new index per line
					# TODO: clean up
					# TODO: do þe todo, it's very ugly...
					# TODO: lists parameters
					elif allows1:
						f  = False # first
						ol = IsOL(data[i:])
						ul = IsUL(data[i:])
						tl = IsTL(data[i:])
						# rl = IsRl(data[i:])
						# print('\x1B[41m', ol, '\x1B[0m')

						if   tl != -1:
							if not len(lists) or lists[-1][0] != 2:
								if len(lists):
									html += ['</li></ul>', '</li></ol>',
										'</label></fieldset>', '</li></ol>'][lists[-1][0]]
									lists.pop(-1)
								lists.append([2, tabs])
								html += "<fieldset class='task-list'>"
								f = True
							newls = True
							if not f: html += '</label>'
							else: f = False
							html += '**FUTURE MAGIC!**'
						elif ul:
							"""if not len(lists) or lists[-1][0] != 0 and lists[-1][1] == tabs:
								if len(lists): # only happens if the previous list is different
									html += LsEnding(lists[-1][0])
									lists.pop(-1)
								lists.append([0, tabs])
								html += f"<ul> <!-- {tabs} tab(s) -->\n"
								f = True
							elif len(lists) and lists[-1][1] < tabs:
								lists.append([0, tabs])
								html += f"<ul> <!-- {tabs} tab(s) -->\n"
								f = True
							elif len(lists) and lists[-1][1] > tabs:
								p = lists.pop(-1)
								f = True
								html += LsEnding(p[0])
							else:
								lists.append([0, tabs])
							newls = True
							if not f: html += '\t</li>'
							else: f = False
							html += '\t<li>'"""

							html += LsAddHeader(lists, 0, tabs)
							newls = True
							i    += 1
						elif ol[0]:
							html += LsAddHeader(lists, 1, tabs)
							newls = True
							i    += ol[1]
						# elif rl:

						# * Heading, one per line
						elif data[i] == '#' and data[i+1] in ' \t\r.#':
							head = data[i:].split(' ', 1)[0]

							if   head == '#.':     head = 'hsmall'; i += 3
							elif head == '#':      head = 'h1';     i += 2
							elif head == '##':     head = 'h2';     i += 3
							elif head == '###':    head = 'h3';     i += 4
							elif head == '####':   head = 'h4';     i += 5
							elif head == '#####':  head = 'h5';     i += 6
							elif head == '######': head = 'h6';     i += 7
							else: head = ''

							if head:
								html += f'<{head}>'

							allows1 = False

						# * Details


					# * Tags
					# (data[i+1] == ',' or not data[i+1] in _reserved)
					if data[i] == '#' and data[i+1] not in _reserved:
						tag = GetValid(data[i+1:])
						ret = ('#' + tag) if data[i+1] != ',' else ''

						if data[i+1] == ',':
							ret == ''

						html += f"<span id='{tag}'>{ret}</span>"

						i += len(ret)
						allows1 = False

					# * Styles
					elif data[i] in '`~^*_=':
						if   data[i:i+2] == '**':  html += AddStyle('strong', styles); i += 2; continue
						elif data[i:i+2] == '==':  html += AddStyle('mark',   styles); i += 2; continue
						elif data[i:i+2] == '__':  html += AddStyle('ins',    styles); i += 2; continue
						elif data[i:i+2] == '~~':  html += AddStyle('strike', styles); i += 2; continue
						elif data[i]     == '*':   html += AddStyle('em',     styles); i += 1; continue
						elif data[i]     == '=':   html += AddStyle('half',   styles); i += 1; continue
						elif data[i]     == '_':   html += AddStyle('sub',    styles); i += 1; continue
						elif data[i]     == '`':   html += AddStyle('code',   styles); i += 1; continue
						elif data[i]     == '^':   html += AddStyle('sup',    styles); i += 1; continue


						allows1 = False
					# * Separations, one per line
					elif data.strip() == '---':
						html += '<hr>\t<!-- ================================================================ -->'
						break
					# * Content


					# * Footnotes
					# * Basic tables



				if data[i] != '\n':
					html += data[i]
				if data[i] not in _reserved:
					allows1 = False
				i += 1

		except:
			print(f"\x1B[44mError on line {j}\x1B[0m")
			pass

		if head:
			html += f'</{head}>'
			head  = ''

		allows1 = True
		html   += '\n'

		j   += 1
		text = file.readline()

	return html


def main(args):
	input      = ''
	output     = 'Output.mr'
	format     = 0 # 0: HTML, 1: PDF, 2: SVG, 3: PNG, 4: EPUB
	stylesheet = None

	if len(args) < 2:
		print("MarkRight requirers at least 1 argument")
		print("Use -h if you need help")
		return -1

	i = 1
	while i < len(args):
		if args[i][0] == '-':
			match args[i][1:]:
				case 'h':
					Parse("./Syntax.mr")
				case 'o':
					if i < len(args)-1:
						output = args[i+1]
						i += 1
					else:
						print("MarkRight requires one more arguments after '-o'")


				case 'f':
					if i < len(args)-1:
						if   args[i+1] == "html": format = 0
						elif args[i+1] == "pdf":  format = 1
						elif args[i+1] == "svg":  format = 2
						elif args[i+1] == "png":  format = 3
						elif args[i+1] == "epub": format = 4
						else:
							print(f"Wrong format parameter on position {i+1}")

						i += 1

				case 's':
					if i < len(args)-1:
						stylesheet = args[i+1]
		else:
			input = args[i]

		i += 1

	print(f"{input}, {output}\n{format}, {stylesheet}")


	# * Just some performance stuff
	from time import time
	start = time()

	html = Parse(input)

	o = open(output, 'w')
	o.write(html)

	print(f"Program finished in {time() - start} seconds.")


	return 0



if __name__ == "__main__":
	from sys import argv
	main(argv)
