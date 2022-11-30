_reserved = " \t\n\r\"!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
_tab      = '\t' # FEKKIN F-STRING RULEZ!!!
_ln       = '\n'
_taskcnt  = 0
_cnNull   = '\x1B[0m'
_cnRed    = '\x1B[41m'
_cnBlue   = '\x1B[44m'

_htmlDocPart1 = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
"""
# After title, style and script if any
_htmlDocPart2 = "</head>\n<body>"
_htmlDocPart3 = """
</body>
<script>
	// https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/checkbox
	// https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset
	// https://developer.mozilla.org/en-US/docs/Web/API/Element/getElementsByClassName
	function TLSetState(task, state) {
		switch(state) {
			case 0: task.checked = false; task.indeterminate = false; break;
			case 1: task.checked = false; task.indeterminate = true;  break;
			case 2: task.checked = true;  task.indeterminate = false; break;
		}
	}

	const everyTaskCheckbox = document.querySelectorAll(".task-list > li > input");
	for(let i=0; i < everyTaskCheckbox.length; i++) {
		switch(everyTaskCheckbox[i].dataset.state) {
			case "unchecked":    TLSetState(everyTaskCheckbox[i], 0); break;
			case "intermediate": TLSetState(everyTaskCheckbox[i], 1); break;
			case "checked":      TLSetState(everyTaskCheckbox[i], 2); break;
		}
	}
</script>
</html>
"""


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
		if data[2:5] == '[ ]': return 0
		if data[2:5] == '[-]': return 1
		if data[2:5] == '[x]': return 2
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
			f"{_tab * tabe}</li>\n{_tab * tabh}</ul>",
			f"{_tab * tabe}</li>\n{_tab * tabh}</ol>"][index]
	except IndexError:
		return ''
def LsStart(index, tabs) -> str:
	try:
		return [
			_ln + f"{_tab * tabs}<ul>" + _ln,
			_ln + f"{_tab * tabs}<ol>" + _ln,
			_ln + f"{_tab * tabs}<ul class='task-list'>" + _ln,
			_ln + f"{_tab * tabs}<ol class='ref-list'>" + _ln][index]
	except IndexError:
		return ''


# TODO: add params
def LsAddHeader(ls: list, type: int, tabs: int, param: int = -1) -> str:
	html  = f'{_tab * (tabs+1)}</li>{_ln}'

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
	# lol no  # function `AddTLTag()`

	if type == 2:
		global _taskcnt
		_taskcnt += 1
		state     = ''

		try: state = ['unchecked', 'intermediate', 'checked'][param]
		except IndexError: pass


		return html + f"{_tab * (tabs+1)}<li>" \
			f"<input type='checkbox' data-state='{state}' name='__MR_TASK_{_taskcnt}'>" \
			f"{_ln}{_tab * (tabs+1)}"
	else:
		return html + f"{_tab * (tabs+1)}<li>" \
			f"{_ln}{_tab * (tabs+1)}"


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
	links = 0     # 0: none, 1: basic, 2: image, 3: wikilink, 4: image-wikilinks, 5: preview

	allows1 = True # allow lists, blockquotes, headings, separators to be written.
	               # False when text is encountered

	j = 0

	while text:
		data, tabs, spaces, after = StripWhiteSpaces(text)

		i  = 0

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
					# TODO: lists parameters
					elif allows1:
						f  = False # first
						ol = IsOL(data[i:])
						ul = IsUL(data[i:])
						tl = IsTL(data[i:])
						# rl = IsRl(data[i:])
						# print('\x1B[41m', ol, '\x1B[0m')

						if   tl != -1:
							html += LsAddHeader(lists, 2, tabs, tl)
							newls = True
							i    += 5
						elif ul:
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
					# TODO: do tag closing for all
					elif data.strip() == '---':
						html += '<hr>\t<!-- ================================================================ -->'
						break

					# stuff
					elif data[i:i+2] == '--':
						html += '—'
						i    += 2
						continue
					elif data[i:i+3] == '...':
						html += '…'
						i    += 3
						continue

				elif not codeb:
					# * Content
					# 1. Detect the start
					# 1. Set the flags
					# 1. Find the end
					# 1. And do more things!
					# --
					# 1. Managing the style inside.
					if   data[i:i+2] == '[[':	pass
					elif data[i:i+1] == '[':	pass
					elif data[i:i+3] == '![[':	pass
					elif data[i:i+3] == '?[[':	pass
					elif data[i:i+2] == '![':	pass

					# * Footnotes
					# * Basic tables



				if data[i] != '\n':
					html += data[i]
				if data[i] not in _reserved:
					allows1 = False
				i += 1

		except:
			print(f"{_cnBlue}Error on line {j}{_cnNull}")
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

	html = _htmlDocPart1 + _htmlDocPart2 + Parse(input) + _htmlDocPart3

	o = open(output, 'w')
	o.write(html)

	print(f"Program finished in {time() - start} seconds.")


	return 0



if __name__ == "__main__":
	from sys import argv
	main(argv)
