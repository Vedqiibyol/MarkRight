_tab       = '\t' # FEKKIN F-STRING RULEZ!!!
_ln        = '\n'

_cnBold    = '\x1B[1m'
_cnHlfb    = '\x1B[2m'
_cnIns     = '\x1B[4m'

_cnNull    = '\x1B[0m'

_cnBlackf  = '\x1B[30m'
_cnRedf    = '\x1B[31m'
_cnGreenf  = '\x1B[32m'
_cnBrownf  = '\x1B[33m'
_cnBluef   = '\x1B[34m'
_cnMagentf = '\x1B[35m'
_cnCyanf   = '\x1B[36m'
_cnWhitef  = '\x1B[37m'
_cnOrangef = '\x1B[38;2;221;114;0m'

_cnBlackB  = '\x1B[40m'
_cnRedB    = '\x1B[41m'
_cnGreenB  = '\x1B[42m'
_cnBrownB  = '\x1B[43m'
_cnBlueB   = '\x1B[44m'
_cnMagentB = '\x1B[45m'
_cnCyanB   = '\x1B[46m'
_cnWhiteB  = '\x1B[47m'
_cnOrangeB = '\x1B[48;2;221;114;0m'

_defStyleR = []

"""_defStyleR = [
	'dragonik',

	'textura', 'textura-dark', 'textura-light'

	'dark-serif',          'dark-roboto',          'dark-roman',          'dark-mono',
	'light-serif',         'light-roboto',         'light-roman',         'light-mono',

	'dark-red-serif',      'dark-red-roboto',      'dark-red-roman',      'dark-red-mono',
	'dark-blue-serif',     'dark-blue-roboto',     'dark-blue-roman',     'dark-blue-mono',
	'dark-green-serif',    'dark-green-roboto',    'dark-green-roman',    'dark-green-mono',
	'dark-purple-serif',   'dark-purple-roboto',   'dark-purple-roman',   'dark-purple-mono',
	'dark-magenta-serif',  'dark-magenta-roboto',  'dark-magenta-roman',  'dark-magenta-mono',
	'dark-pink-serif',     'dark-pink-roboto',     'dark-pink-roman',     'dark-pink-mono',
	'dark-cyan-serif',     'dark-cyan-roboto',     'dark-cyan-roman',     'dark-cyan-mono',

	'light-red-serif',     'light-red-roboto',     'light-red-roman',     'light-red-mono',
	'light-blue-serif',    'light-blue-roboto',    'light-blue-roman',    'light-blue-mono',
	'light-green-serif',   'light-green-roboto',   'light-green-roman',   'light-green-mono',
	'light-purple-serif',  'light-purple-roboto',  'light-purple-roman',  'light-purple-mono',
	'light-magenta-serif', 'light-magenta-roboto', 'light-magenta-roman', 'light-magenta-mono',
	'light-pink-serif',    'light-pink-roboto',    'light-pink-roman',    'light-pink-mono',
	'light-cyan-serif',    'light-cyan-roboto',    'light-cyan-roman',    'light-cyan-mono',

	'dark-researchpaper',
	'light-researchpaper',
]"""

def PrintErr(*args: object, sep: str ='', end: str ='') -> None:
	""" This function prints given text with an error, or red foreground. """
	print(_cnRedf, *args, _cnNull, sep=sep, end=end)
def PrintWarn(*args: object, sep: str ='', end: str ='') -> None:
	""" This function prints given text with a warning, or orange foreground. """
	print(_cnOrangef, *args, _cnNull, sep=sep, end=end)
def PrintVoc(*args: object, sep: str ='', end: str ='') -> None:
	""" This function prints given text a green foreground. """
	print(_cnBold, _cnGreenf, *args, _cnNull, sep=sep, end=end)
def PrintLite(*args: object, sep: str ='', end: str ='') -> None:
	""" This function prints given text with a half-bright font weight. """
	print(_cnHlfb, *args, _cnNull, sep=sep, end=end)
def PrintBold(*args: object, sep: str ='', end: str ='') -> None:
	""" This function prints given text with a bold font weight. """
	print(_cnBold, *args, _cnNull, sep=sep, end=end)
def Print(*args: object, sep: str ='', end: str ='') -> None:
	print(*args, sep=sep, end=end)


_reserved = " \t\n\r\"!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
_taskcnt  = 0
lsbr      = 0


_htmlDocPart1 = """<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
"""
# After title, style and script if any
_htmlDocPart2 = "</head>\n<body>\n"
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
def IsOL(data) -> tuple[bool, int, int]:
	cnt = 0
	num = ''
	end = data.find('.')

	if end != -1:
		num = data[:end]
		for i in num:
			if i in _reserved or not i.isdigit(): return [False, -1, None]
			cnt += 1
		if cnt:
			return [True, cnt+1, int(num)]

	return [False, -1, None]
def IsRL(data) -> tuple[bool, int, str]:
	cnt = 0
	txt = ''
	end = data.find(']:')

	if data[0] == '[' and end != -1:
		txt = data[1:end]
		for i in txt:
			if i in _reserved: return [False, -1, None]
			cnt += 1
		return [True, cnt + 3, txt]

	return [False, -1, None]

def LsEnding(index, tabs=0) -> str:
	tabh = tabs
	tabe = tabs + 1

	try:
		return [
			f"{_tab * tabe}</li>\n{_tab * tabh}</ul>\n",
			f"{_tab * tabe}</li>\n{_tab * tabh}</ol>\n",
			f"{_tab * tabe}</li>\n{_tab * tabh}</ul>\n",
			f"{_tab * tabe}</li>\n{_tab * tabh}</ol>\n"][index]
	except IndexError:
		return ''
def LsStart(index, tabs, param=None) -> str:
	try:
		return [
			_ln + f"{_tab * tabs}<ul>" + _ln,
			_ln + f"{_tab * tabs}<ol>" + _ln,
			_ln + f"{_tab * tabs}<ul class='task-list'>" + _ln,
			_ln + f"{_tab * tabs}<ul class='ref-list'>" + _ln][index]
	except IndexError:
		return ''
# TODO: add params
def LsAddHeader(ls: list, type: int, tabs: int, param=None) -> str:
	html  = f'{_tab * (tabs+1)}</li>{_ln}'

	global lsbr

	if lsbr:
		html += _tab*(tabs+1) + '<br>'*lsbr + '\n'
		lsbr  = 0


	if len(ls):
		if ls[-1][1] > tabs:
			p    = ls.pop(-1)
			html = LsEnding(p[0])
		elif ls[-1][1] < tabs:
			last = ls[-1]
			ls.append([type, tabs])
			html += LsStart(type, tabs, param)
		elif ls[-1][0] != type:
			p     = ls.pop(-1)
			html  = LsEnding(p[0])
			ls.append([type, tabs])
			html += LsStart(type, tabs, param)
	else: # empty list, WTF?
		ls.append([type, tabs])
		html = LsStart(type, tabs, param)

	# TODO: task list with a new function
	# global value for each label
	# lol no  # function `AddTLTag()`

	if type == 2 and param != None:
		global _taskcnt
		_taskcnt += 1
		state     = ''

		try: state = ['unchecked', 'intermediate', 'checked'][param]
		except IndexError: pass


		return html + f"{_tab * (tabs+1)}<li>" \
			f"<input type='checkbox' data-state='{state}' name='__MR_TASK_{_taskcnt}'>" \
			f"{_ln}{_tab * (tabs+1)}"
	elif type == 3 and param != None:
		return html + f"{_tab * (tabs+1)}<li class='ref' id='{param}' data-name='{param}'>"
	else:
		return html + f"{_tab * (tabs+1)}<li>" \
			f"{_ln}{_tab * (tabs+1)}"


# \ **value**
# [0]: none
# [1]: wikilink
# [2]: basic
# [3]: image-wikilinks
# [4]: preview
# [5]: image
# [6]: next argument, for basic links
# [7]: next-arg, second flag
# TODO: preview
def LinkAddSingle(lnk, type) -> str:
	match type:
		case 1: return f"<a href='{lnk}' class='wikilink'>{lnk}</a>"
		case 3: return f"<img src='{lnk}' alt='{lnk}' class='wikilink-image'>"
		case 4: return f"<a href='{lnk}' class='wikilink'>{lnk}</a>"

	return ''
# TODO: do type 5
def LinkAddDouble(lnk, title, type) -> str:
	return f"<a href='{lnk}' class='md-link'>{title}</a>"

def Parse(input):
	file = open(input)
	text = file.readline()
	html = ['']

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
		'half'   : False,
		'q'      : False
	}

	global lsbr

	head     = ''    # only one per line
	lists    = []    # not that if non-empty, no <br> should be added
	newls    = False # new list
	quote    = 0
	# perhaps
	# qlscnt   = []
	codeb    = None
	code     = False
	links    = 0     # 0: none, 1: wikilink, 2: basic, 3: image-wikilinks, 4: preview, 5: image, 6: options

	paragrph = 0
	allows1  = True # allow lists, blockquotes, headings, separators to be written.
	               # False when text is encountered
	lnktitle = ''
	lnktype  = 0
	detail   = 0

	j = 1

	# TODO: fekking clean up, this is a mess!

	while text:
		data, tabs, spaces, after = StripWhiteSpaces(text)

		i  = 0

		try:
			# * Line breaks
			# TODO: make it with <p> but just a tag better LOL
			if len(data) <= 1:
				if (      paragrph and not codeb and
					not head     and not quote and
					not detail   and not len(lists)):
					html[-1] += '</p>\n'
					paragrph -= 1
				elif not len(lists):
					html[-1] += '<br>'

			while i < len(data): # ``while len(text)``
				# * Separations, one per line
				# TODO: do tag closing for all
				if not code and not codeb and data.strip() == '---':
					html[-1] += '<hr>\t<!-- ================================================================ -->'
					break

				# * black magic involving lists
				if len(data) <= 1 and len(lists) and not codeb:
					lsbr += 1
				if len(lists) and tabs < lists[-1][1] and len(data) > 1:
					for i in range(lists[-1][1] - tabs):
						html[-1] += LsEnding(lists.pop(-1)[0])

				# * Code block
				if   data[i:i+3] == '```':
					if codeb == None:
						codeb = GetValid(data[i:].strip())
						if codeb == None or not len(codeb):
							codeb = 'txt'

						# TODO: TinyMCE
						html[-1] += f"<textarea class='codeblock' data-lang='{codeb}'>\n"

						allows1 = False
					else:
						codeb    = None
						allows1  = False
						html[-1] += "</textarea> <!-- end of codeblock --> <br>"
					i += 3
				elif data[i:i+2] == '``':
					code     ^= 1
					html[-1] += '<' + ('/'*(not code)) + 'code>'
					i        += 2
					allows1   = False

				# ! Should blockquotes really be paragraph inhibiter?
				# * Blockquotes
				if not code and not codeb:
					if   data[i:][:2] == '<<':
						html[-1] += '<blockquote>\n'
						i        += 2
						quote    += 1
					elif data[i:][:2] == '>>' and quote:
						quote    -= 1
						html[-1] += '\n</blockquote>\n'
						i        += 2

				# * Ref-lists
				if not code and not codeb and allows1:
					# .{1}
					rl = IsRL(data[i:])
					if rl[0]:
						html[-1] += LsAddHeader(lists, 3, tabs, rl[2])
						newls = True
						i += rl[1]

				# * Detail section
				if not code and not codeb:
					if data[i:i+2] == '((':
						detail   += 1
						html[-1] += '<details>'
						i        += 2
						summary   = data[i+1:]
						if summary:
							html[-1] += f'<summary>{summary}</summary>'
							i        += len(summary)
					if detail and data[i:i+2] == '))':
						detail   -= 1
						html[-1] += '</details>'
						i        += 2

				# * Lists, on new index per line
				# TODO: lists parameters
				if not code and not codeb and allows1:
					f  = False # first
					ol = IsOL(data[i:])
					ul = IsUL(data[i:])
					tl = IsTL(data[i:])

					if   tl != -1:
						html[-1] += LsAddHeader(lists, 2, tabs, tl)
						newls = True
						i    += 5
					elif ul:
						html[-1] += LsAddHeader(lists, 0, tabs)
						newls = True
						i    += 1
					elif ol[0]:
						html[-1] += LsAddHeader(lists, 1, tabs, ol[2])
						newls = True
						i    += ol[1]

				# * Heading, one per line
				if not code and not codeb and allows1:
					if data[i] == '#' and data[i+1] in ' \t\r.#':
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
							html[-1] += f'<{head}>'

						allows1 = False



				# * Paragraphs
				if  (len(data) > 1 and
					not paragrph and not codeb and
					not head     and not quote and
					not detail   and not len(lists)):
					html[-1] += '\n<p>'
					allows1   = False
					paragrph += 1

				# later:
				# * Inline HTML styling

				# * Content
				# TODO: work images for width/length, etc
				# TODO: work the add-ons (youtube:// twitch:// steam:// github://)
				# TODO: perhaps `Parse` needs to be redone to accept single
				# TODO: strings in order to parse extracted strings from `[]`
				if not code and not codeb:
					# 1. Detect the start
					# 1. Set the flags
					# 1. Find the end
					# 1. And do more things!
					# --
					# 1. Managing the style inside.
					# --
					# \ **value**
					# [0]: none
					# [1]: wikilink
					# [2]: basic
					# [3]: image-wikilinks
					# [4]: preview
					# [5]: image
					# [6]: next argument, for basic links
					# [7]: next-arg, second flag
					if links == 0 and data[i:i+3] == '![[':
						src       = data[i+3:data.find(']]')]
						html[-1] += LinkAddSingle(src, 3)
						i        += len(src) + 5
					if links == 0 and data[i:i+3] == '?[[':
						src       = data[i+3:data.find(']]')]
						html[-1] += LinkAddSingle(src, 4)
						i        += len(src) + 5
					if links == 0 and data[i:i+2] == '[[':
						src       = data[i+2:data.find(']]')]
						html[-1] += LinkAddSingle(src, 1)
						i        += len(src) + 4

					if links == 0 and data[i] == '[': links = 2; html.append(''); i += 1; lnktype = 2
					if links == 0 and data[i:i+1] == '![': links = 2; html.append(''); i += 1; lnktype = 5

					if links == 2 and data[i] == ']':
						links = 6
						lnktitle = html.pop(-1)
						i += 1

					if links == 6 and data[i] == '(':
						src       = data[i+1:data.find(')')]
						links     = 0
						i        += 1 + len(src) + 1
						html[-1] += LinkAddDouble(src, lnktitle, lnktype)


				# * Tags
				if not code and not codeb:
					# (data[i+1] == ',' or not data[i+1] in _reserved)
					if data[i] == '#' and data[i+1] not in _reserved:
						tag = GetValid(data[i+1:])
						ret = ('#' + tag) if data[i+1] != ',' else ''

						if data[i+1] == ',':
							ret == ''

						html[-1] += f"<span id='{tag}'>{ret}</span>"

						i += len(ret)
						allows1 = False

				# * Styles
				if not code and not codeb and data[i] in "`~^*_='":
					if   data[i:i+2] == '**':  html[-1] += AddStyle('strong', styles); i += 2; continue
					elif data[i:i+2] == '==':  html[-1] += AddStyle('mark',   styles); i += 2; continue
					elif data[i:i+2] == '__':  html[-1] += AddStyle('ins',    styles); i += 2; continue
					elif data[i:i+2] == '~~':  html[-1] += AddStyle('strike', styles); i += 2; continue
					elif data[i:i+2] == "''":  html[-1] += AddStyle('q',      styles); i += 2; continue
					elif data[i]     == '*':   html[-1] += AddStyle('em',     styles); i += 1; continue
					elif data[i]     == '=':   html[-1] += AddStyle('half',   styles); i += 1; continue
					elif data[i]     == '_':   html[-1] += AddStyle('sub',    styles); i += 1; continue
					elif data[i]     == '`':   html[-1] += AddStyle('code',   styles); i += 1; continue
					elif data[i]     == '^':   html[-1] += AddStyle('sup',    styles); i += 1; continue


					allows1 = False

				# * Miscellaneous ('--', '...')
				if not code and not codeb:
					if data[i:i+2] == '--':
						html[-1] += '—'
						i    += 2
						continue
					elif data[i:i+3] == '...':
						html[-1] += '…'
						i    += 3
						continue


				# * Footnotes
				# * Basic tables

				if data[i] != '\n':
					html[-1] += data[i]
				if data[i] not in _reserved:
					allows1 = False
				i += 1

		except IndexError:
			print(f"{_cnBlueB}Error on line {j}{_cnNull}")
			pass

		if head:
			html[-1] += f'</{head}>'
			head  = ''

		allows1  = True
		html[-1] += '\n'

		j    += 1
		links = 0
		text  = file.readline()

	return html[0]


def PrintInfo(info):
	# input
	PrintLite('input=')
	PrintBold(info['input'])

	# output
	PrintLite(', output=')
	PrintBold(info['output'])
	if info['noOutput']:
		PrintWarn(' (Default)')

	print()

	# stylesheet
	PrintLite('stylesheet=')
	if len(info['stylesheet']):
		PrintBold(info['stylesheet'])
	else:
		PrintWarn('None')

	PrintLite(', stylesheet-bundle=')
	if len(info['stylebundle']):
		PrintBold(info['stylesbundle'])
	else:
		PrintWarn('None')

	print()

	# default stylesheet
	PrintLite('default-stylesheet=')
	if len(info['def-stylesheet']):
		PrintBold(info['def-stylesheet'])
	else:
		PrintWarn('None')

	PrintLite(', default-stylesheet-bundle=')
	if len(info['def-stylebundle']):
		PrintBold(info['def-stylebundle'])
	else:
		PrintWarn('None')

	print()

	# format
	PrintLite('format=')
	PrintBold(info['format'])
	PrintVoc(f" {['HTML','PDF','SVG','PNG','EPUB'][info['format']]}")

	print()

def FindStyleSheet(name: str, default: bool) -> str:
	import os
	if default:
		if i in _defStyleR:
			return 'stylesheet/' + i + '.css'
		else:
			PrintErr(f"There is no default stylesheet named '{name}'")
			return ''
	else:
		if os.path.isfile(name): return name
		else: ''
def AddStylesheet(name: str, bundle: bool) -> str:
	if not bundle:
		return f"<link rel='stylesheet' href='{name}'>"
	else:
		f = open(name)
		return f"""<style>
		{f.read(-1)}
		</style>"""

def main(args):
	info = {
		'input':           '',
		'output':          'Output.mr',
		'noOutput':        True,
		'format':          0, # 0: HTML, 1: PDF, 2: SVG, 3: PNG, 4: EPUB
		'stylesheet':      [],
		'stylebundle':     [],
		'def-stylesheet':  [],
		'def-stylebundle': []
	}

	isSetInput    = False
	isSetOutput   = False

	styleLinks    = []
	styleBunbdles = []


	if len(args) < 2:
		print("MarkRight requirers at least 1 argument")
		print("Use -h if you need help")
		return -1

	i = 1
	while i < len(args):
		if args[i][0] == '-':
			hasleft = len(args) - (i+1)
			match args[i][1:]:
				case 'h':
					# OpenHelp()
					PrintMan()
					return 1
				case 'o':
					if isSetOutput:
						PrintErr("You have already given an output!")
					if hasleft:
						info['output']   = args[i+1]
						info['noOutput'] = False
						isSetOutput      = True
						i               += 1
					else:
						PrintErr("MarkRight requires one more arguments after '-o'")
				case 'f':
					if hasleft:
						if   args[i+1] == "html": info['format'] = 0
						elif args[i+1] == "pdf":  info['format'] = 1
						elif args[i+1] == "svg":  info['format'] = 2
						elif args[i+1] == "png":  info['format'] = 3
						elif args[i+1] == "epub": info['format'] = 4
						else:
							PrintErr(f"Wrong format parameter on position {i+1}")

						i += 1
					else:
						PrintErr("MarkRight requires one more arguments after '-f'\n")
				case 's':
					if hasleft:
						info['stylesheet'].append(args[i+1])

						path = FindStyleSheet(args[i+1], False)
						if path:
							styleLinks.append(AddStylesheet(args[i+1], False))
						else:
							PrintErr(f"Could not find stylesheet '{args[i+1]}'\n")

						i += 1
					else:
						PrintErr("MarkRight requires one more arguments after '-s'\n")
				case 'sb': # style bundle
					if hasleft:
						info['stylebundle'].append(args[i+1])

						path = FindStyleSheet(args[i+1], False)
						if path:
							styleBunbdles.append(AddStylesheet(args[i+1], True))
						else:
							PrintErr(f"Could not find default style '{args[i+1]}'\n")

						i += 1
					else:
						PrintErr("MarkRight requires one more arguments after '-sb'\n")
				case 'ds': # custom style
					if hasleft:
						info['stylesheet'].append(FindStyleSheet(args[i+1], True))
						i += 1
					else:
						PrintErr("MarkRight requires one more arguments after '-cs'\n")
				case 'dsb': # custom style bundle
					pass
				case 'lds':
					if len(_defStyleR):
						PrintBold(f"Default styles:\n\t")
						for i, n in enumerate(_defStyleR):
							Print(n, '\t', '\n\t' if (i%3) else '')
						print()
					else:
						PrintErr("Did not found any default styles, please update are report to issue!")
					return 1
				# case 'lf': pass

				case _: PrintErr(f"Unknown argument `{args[i]}`\n")
		else:
			info['input'] = args[i]

		i += 1

	PrintInfo(info)

	# * Just some performance stuff
	from time import time_ns
	start = time_ns()

	htmlStylesL = ''
	htmlStylesB = ''

	for i in styleLinks:
		htmlStylesL += i + '\n'
	for i in styleBunbdles:
		htmlStylesB += '<styles>\n' + i + '\n</styles>\n'

	html = _htmlDocPart1 + htmlStylesL + _htmlDocPart2 + Parse(info['input']) + _htmlDocPart3 + htmlStylesB + '</html>'

	o = open(info['output'], 'w')
	o.write(html)

	Print('Program finished in ')
	PrintVoc(time_ns() - start)
	Print(' nano-seconds.', end='\n')


	return 0

def PrintMan():
	print(f"""{_cnBold}MarkRight

Usage:
	{_cnHlfb}${_cnNull+_cnBold} python main-2022-11-23.py <str> [option] (<str|int>)

Commands:{_cnNull}
	{_cnBold}-h{_cnNull}	Print this help.
	{_cnBold}-o   {_cnHlfb}…{_cnNull}	Give an output file.
	{_cnBold}-f   {_cnHlfb}…{_cnNull}	Give an output format.
	{_cnBold}-s   {_cnHlfb}…{_cnNull}	Give stylesheets.
	{_cnBold}-sb  {_cnHlfb}…{_cnNull}	Bundles stylesheet inside the output HTML.
	{_cnBold}-ds  {_cnHlfb}…{_cnNull}	Custom style sheet.
	{_cnBold}-dsb {_cnHlfb}…{_cnNull}	Bundle default stylesheet inside the output HTML.
	{_cnBold}-lds{_cnNull}	List all default styles.

For more information please read Syntax.mr:
{_cnBold}{_cnHlfb}${_cnNull+_cnBold} python main-2022-11-23.py Syntax.mr -o Syntax.html{_cnNull}""")
	# {_cnBold}-lf{_cnNull}	List all formats


if __name__ == "__main__":
	import os
	for i in os.listdir('./stylesheets/'):
		if os.path.isfile(i) and i.endswith('.css') and len(i) > 4:
			_defStyleR.append(i[:-4])
	# print(_defStyleR)

	from sys import argv
	main(argv)
