#!/usr/bin/python
import re

_tab       = '\t' # FEKKIN F-STRING RULEZ!!!
_ln        = '\n'

_theme     = 'dark' # light | dark
_disp      = 'grid' # grid  | list

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

reHead         = re.compile(r'(\#{1,6}|\#\.)\s+')
reTag          = re.compile(r'\#(,?)(?P<tag>\w+)')
reUL           = re.compile(r'^(-\s+)')
reOL           = re.compile(r'^(\d+)\.\s+')
reTL           = re.compile(r'^-\s+\[(x|-| )\]\s+')
reRL           = re.compile(r'^\[(\w+)\]\:\s+')
reForceCode    = re.compile(r'`{2}')
reCode         = re.compile(r'`{3}\s*(?P<lang>\w*)?$')
reCodeClose    = re.compile(r'`{3}')
reDetail       = re.compile(r'\({2}\s*(?P<summary>.+)?$')
reDetailClose  = re.compile(r'\){2}')
reStyle        = re.compile(r'(!{2}|\|{2}|\*{1,2}|={1,2}|_{1,2}|~{2}|\'{2}|`|\^)')
reWikilink     = re.compile(r'(?P<img>(\!|\?))?\[{2}(?P<data>(.+))\]{2}')
reContentLink  = re.compile(r'\]\s*\(((.+))\)')
reEmail        = re.compile(r'(?P<name>.+)@(?P<url>\w+(\.\w+))+')
reLink         = re.compile(r'(https?\:\/\/)?(?P<url>((\S+\.\S+)+\/*))')
reGrids        = re.compile(r'{{\s*(?P<title>.+)?')
reGridsClose   = re.compile(r'}}')
reGridCel      = re.compile(r'<{\s*(?P<title>.+)?')
reGridCelClose = re.compile(r'}>')
reLaTeX        = re.compile(r'\${2}\s*(?P<title>.+)?')
# reList         = re.compile(r'((?P<ol>(\d+)\.\s+)|(?P<tl>-\s+\[(x|-| )\]\s+)|(?P<ul>(-\s+))|(?P<rl>\[(\w+)\]\:\s+))')

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


def LsEnding(index, tabs=0) -> str:
	tabh = tabs
	tabe = tabs + 1

	try:
		return {
			'ul': f"{_tab * tabe}</li>\n{_tab * tabh}</ul>\n",
			'ol': f"{_tab * tabe}</li>\n{_tab * tabh}</ol>\n",
			'tl': f"{_tab * tabe}</li>\n{_tab * tabh}</ul>\n",
			'rl': f"{_tab * tabe}</li>\n{_tab * tabh}</ul>\n"}[index]
	except IndexError:
		return ''
def LsStart(index, tabs, param=None) -> str:
	try:
		return {
			'ul': _ln + f"{_tab * tabs}<ul>" + _ln,
			'ol': _ln + f"{_tab * tabs}<ol>" + _ln,
			'tl': _ln + f"{_tab * tabs}<ul class='task-list'>" + _ln,
			'rl': _ln + f"{_tab * tabs}<ul class='ref-list'>" + _ln}[index]
	except IndexError:
		return ''
# TODO: add params
def LsAddHeader(ls: list, type: int, tabs: int, param=None) -> str:
	tabs += 1

	html = f'{_tab * (tabs+1)}</li>{_ln}'
	nls  = False

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
			nls = True
		elif ls[-1][0] != type:
			p     = ls.pop(-1)
			html  = LsEnding(p[0])
			ls.append([type, tabs])
			html += LsStart(type, tabs, param)
			nls = True
	else: # empty list, WTF?
		ls.append([type, tabs])
		html = LsStart(type, tabs, param)


	if type == 'ol' and param != None and nls:
		return html + f"<li value='{param}'>{_ln}{_tab * (tabs+1)}"
	elif type == 'tl' and param != None:
		global _taskcnt
		_taskcnt += 1
		state     = ''

		try: state = ['unchecked', 'intermediate', 'checked'][param]
		except IndexError: pass


		return html + f"{_tab * (tabs+1)}<li>" \
			f"<input type='checkbox' data-state='{state}' name='__MR_TASK_{_taskcnt}'>" \
			f"{_ln}{_tab * (tabs+1)}"
	elif type == 'rl' and param != None:
		return html + f"{_tab * (tabs+1)}<li class='ref' id='{param}' data-name='{param}'>"
	else:
		return html + f"{_tab * (tabs+1)}<li>" \
			f"{_ln}{_tab * (tabs+1)}"

# - [-] youtube.com -- channels and social
# - [-] youtu.be    -- same
# - [x] twitch
# - [ ] steam
# - [ ] twitter     -- iframe of script
# - [-] reddit      -- r/x
# - [ ] spotify
# - [ ] deezer
# - [ ] github
# - [ ] wikipedia
# - [ ] discord
# - [ ] google
# - [ ] gdrive
# - [ ] dropbox
# - [ ] gmail
# - [ ] megacloud
# * It would be better to be able to directly copy the link of the video.
# * Most people don't just copy one lil bit of the URL.
# * Maybe not the share feature, although it could be done...
def AddLink(title: str, lnk: str, params: dict, img: None | str) -> str:
	if img == None: return f"<a href='{lnk}'>{title}</a>"
	elif img == '!':
		if (m := re.match(r'(https?\:\/\/)?(www\.)?(?P<app>\w+\.\w+)\/(?P<path>.+)', lnk)):
			if m.group('app') == 'youtube.com':
				ret = m.group('path')
				if (z := re.match(r'(?P<t>watch\?v=|playlist\?list=)(?P<id>.+)\/', m.group('path'))):
					match z.group('t'):
						case 'watch?v=':       ret = z.group('id')
						case 'playlist?list=': ret = f"videoseries?list={z.group('id')}"

				return f"""<iframe width="{params['width']}" height="{params['height']}" \
				src="https://www.youtube.com/embed/{ret}" \
				title="{title if title else 'YouTube video player'}" \
				frameborder="0" allow="accelerometer; autoplay; \
				clipboard-write; encrypted-media; gyroscope; \
				picture-in-picture" allowfullscreen \
				class="mr-app mr-youtube {params['put']}"></iframe>"""
			elif m.group('app') == 'youtu.be':
				return f"""<iframe width="{params['width']}" height="{params['height']}" \
				src="https://www.youtube.com/embed/{path}" \
				title="{title if title else 'YouTube video player'}" \
				frameborder="0" allow="accelerometer; autoplay; \
				clipboard-write; encrypted-media; gyroscope; \
				picture-in-picture" allowfullscreen \
				class="mr-app mr-youtube {params['put']}"></iframe>"""
			elif m.group('app') == 'twitch.tv':
				# https://www.twitch.tv/bobross
				z = re.match(r'(?P<channel>.+|video)(\/(?P<video>.+))?', m.group('path'))

				ret  = ('channel' if z.group('channel') != 'video' else 'video')
				ret += '=' + z.group(ret)

				return f"""<iframe height="{params['height']}" width="{params['width']}" \
				src="https://player.twitch.tv/?{ret}&parent=www.example.com" \
				frameborder="0" allowfullscreen="true" scrolling="no" \
				class="mr-app mr-twitch {params['put']}"></iframe>"""
			elif m.group('app') == 'reddit.com':
				# https://www.reddit.com/r/gaming/comments/zuwyxh/kids_now_a_days_will_never_know_the_pain_of/?utm_source=share&utm_medium=web2x&context=3
				# https://www.reddit.com/r/gaming/comments/zuwyxh/kids_now_a_days_will_never_know_the_pain_of/
				return f"""<iframe width="{params['width']}" height="{params['height']}"\
				src="https://www.redditmedia.com/{m.group('path')}?ref_source=embed&amp;ref=share&amp;embed=true&amp;theme={_theme}" \
				sandbox="allow-scripts allow-same-origin allow-popups" \
				style="border: none;" scrolling="no"
				class="mr-app mr-reddit {params['put']}"></iframe>"""
		return f"""<img src='{lnk}' alt='{title}' \
		height='{params['height']}' width='{params['width']}' \
		class='mr-link default-img {params['put']}'>"""
	elif img == '?':  return f"""<iframe src='{lnk}' title='{title}' \
		height='{params['height']}' width='{params['width']}' \
		class='mr-link default-prev {params['put']}'></iframe>"""

	return ''
def LinkParseArgs(src) -> dict:
	params = {'width': '', 'height': '', 'put': ''}

	for p in src:
		if (x := re.match(r'((?P<pos>height|width)=)?(?P<value>\d+)', p)):
			if (pos := x.group('pos')):
				if not params[pos]:  params[pos]      = x.group('value')
			elif not params['height']: params['height'] = x.group('value')
			elif not params['width']:  params['width']  = x.group('value')
		elif (z := re.match(r'put\-(left|right|center)', p)) and not params['put']:
			params['put'] = 'put-' + z.group(1)
		elif (z := re.match(r'(?P<arg>)=(?P<value>.+)')):
			params[z.group('arg')] = z.group('value')

	if not params['height']: params['height'] = 315
	if not params['width']:  params['width']  = 560

	return params

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
	style = {
		'*':  [False, '<em>',   '</em>'],   '**': [False, '<strong>', '</strong>'],
		'_':  [False, '<sub>',  '</sub>'],  '__': [False, '<ins>',    '</ins>'],
		'==': [False, '<mark>', '</mark>'], '^':  [False, '<sup>',    '</sup>'],
		"''": [False, '<q>',    '</q>'],    '~~': [False, '<strike>', '</strike>'],
		'`':  [False, '<code>', '</code>'], '!!': [False, "<span class='high'>", '</span>'],
		'||': [False, "<span class='blur'>", '</span>'],
		'=':  [False, "<span class='half'>", '</span>']
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
	lnkttpos = None
	lnktype  = 0
	detail   = 0

	j = 1

	# TODO: fekking clean up, this is a mess!

	while text:
		data, tabs, spaces, after = StripWhiteSpaces(text)

		i  = 0

		try:
			# * Line breaks and paragraphs
			if len(data) <= 1:
				if (      paragrph and not codeb and
					not head     and not quote and
					not detail   and not len(lists)):
					html += '</p>\n'
					paragrph -= 1
				elif not len(lists):
					html += '<br>'
			if len(lists) and lists[-1][1] > tabs and len(data) > 1:
				if not  (reUL.match(data)
					or reOL.match(data)
					or reTL.match(data)
					or reRL.match(data)):
					for _ in range(lists[-1][1] - tabs):
					# while len(lists) or lists[-1][1] > tabs:
						html += LsEnding(lists.pop(-1)[0])

			while i < len(data): # ``while len(text)``
				# * Separations, one per line
				# TODO: do tag closing for all
				if not code and not codeb and data.strip() == '---':
					html += '<hr>\t<!-- ================================================================ -->'
					break

				# * black magic involving lists
				if len(data) <= 1 and len(lists) and not codeb: lsbr += 1

				# * Code block
				if (m := reCode.match(data[i:])) != None and codeb == None:
					codeb = m.group('lang') if m.groups else 'txt'

					if html[-6:-2] != '</p>' or html[-6:-2] != '<br>': html += '<br>'

					# TODO: Parser

					html   += f"<pre class='codeblock' data-lang='{codeb}'>"
					allows1 = False
					i      += len(m.group(0))
				elif (m := reCodeClose.match(data[i:])) != None and codeb != None:
					allows1 = False
					html   += '</pre>'
					codeb   = None
					i      += 3
				elif (m := reForceCode.match(data[i:])) != None and codeb == None:
					code     ^= 1
					html += '<' + ('/'*(not code)) + 'code>'
					i        += 2
					allows1   = False

				# * Blockquotes
				if not code and not codeb and data[i:i+2] == '<<':
					html += '<blockquote>\n'
					i        += 2
					quote    += 1
				elif not code and not codeb and quote and data[i:i+2] == '<<':
						quote    -= 1
						html += '\n</blockquote>\n'
						i        += 2

				# * Detail section
				if not code and not codeb and (m := reDetail.match(data[i:])):
					detail += 1
					html   += '<details>'
					if m.groups: html += f'<summary>{m.group(1)}</summary>'
					i += len(m.group(0))
				if not code and not codeb and detail and (m := reDetailClose.match(data[i:])):
					detail -= 1
					html   += '</details>'
					i      += len(m.group(0))

				# * Lists, on new index per line
				if not code and not codeb and allows1 and (m := reTL.match(data[i:])) != None:
					html += LsAddHeader(lists, 'tl', tabs, ' -x'.index(m.group(1)))
					newls = True
					i    += len(m.group(0))
				if not code and not codeb and allows1 and (m := reUL.match(data[i:])) != None:
					html += LsAddHeader(lists, 'ul', tabs)
					newls = True
					i    += len(m.group(0))
				if not code and not codeb and allows1 and (m := reOL.match(data[i:])) != None:
					html += LsAddHeader(lists, 'ol', tabs, int(m.group(1)))
					newls = True
					i    += len(m.group(0))
				if not code and not codeb and allows1 and (m := reRL.match(data[i:])) != None:
					html += LsAddHeader(lists, 'rl', tabs, m.group(1))
					newls = True
					i    += len(m.group(0))

				# * Heading, one per line
				if not code and not codeb and allows1 and (m := reHead.match(data[i:])) != None:
					match m.group(1):
						case '#.':     html += "<span class='hsmall'>"; head = '</span>'
						case '#':      html += '<h1>'; head = '</h1>'
						case '##':     html += '<h2>'; head = '</h2>'
						case '###':    html += '<h3>'; head = '</h3>'
						case '####':   html += '<h4>'; head = '</h4>'
						case '#####':  html += '<h5>'; head = '</h5>'
						case '######': html += '<h6>'; head = '</h6>'
					allows1 = False
					i += len(m.group(0))

				# * Paragraphs
				if  (len(data) > 1 and
					not paragrph and not codeb and
					not head     and not quote and
					not detail   and not len(lists)):
					html += '\n<p>'
					allows1   = False
					paragrph += 1

				# later:
				# * Inline HTML styling

				# * Content
				# TODO: perhaps `Parse` needs to be redone to accept single
				# 1. Managing the style inside.
				# --
				# \ **value**
				# [0]: none
				# [1]: wikilink           [[  ]]
				# [2]: basic              [ ]( )
				# [3]: image-wikilinks   ![[  ]]
				# [4]: preview           ?[[  ]]
				# [5]: image             ![ ]( )
				# [6]: next argument, for basic links
				# [7]: next-arg, second flag
				if not code and not codeb and links == 0 and (m := reWikilink.match(data[i:])) != None:
					src   = m.group('data').replace('\t', ' ').split(' ')
					img   = m.group('img')
					html += AddLink(src[0], src[0], LinkParseArgs(src[1:]), img)
					i    += len(m.group(0))

				if not code and not codeb and links == 0 and data[i:i+1] == '[' and lnkttpos == None:
					links    = 1
					lnkttpos = len(html)
					i       += 1
				if not code and not codeb and links == 0 and data[i:i+2] == '![' and lnkttpos == None:
					links    = 2
					lnkttpos = len(html)
					i       += 1

				if not code and not codeb and links and (m := reContentLink.match(data[i:])) != None and lnkttpos != None:
					lnktitle = html[lnkttpos:]
					html     = html[:lnkttpos]
					lnkttpos = None
					src      = m.group(1).replace('\t', ' ').split(' ')
					html    += AddLink(lnktitle, src[0], LinkParseArgs(src[1:]), [None,'!','?'][links-1])
					i       += len(m.group(0))

				# * Tags
				if not code and not codeb and (m := reTag.match(data[i:])) != None:
					tag   = m.group('tag')
					html += f"<span id='{tag}'>{f'#{tag}' if m.group(1) == ',' else ''}</span>"
					i    += len(m.group(0))
					allows1 = False

				# * Styles
				if not codeb and not code and (m := reStyle.match(data[i:])) != None:
					html += style[m.group(1)][1 + style[m.group(1)][0]]
					style[m.group(1)][0] ^= 1
					i    += len(m.group(1))
					allows1 = False
					continue

				# * Miscellaneous ('--', '...')
				if not code and not codeb:
					if data[i:i+2] == '--':
						html += '—'
						i    += 2
						continue
					elif data[i:i+3] == '...':
						html += '…'
						i    += 3
						continue


				# * Footnotes
				# * Basic tables

				if data[i] != '\n':
					html += data[i]
				if data[i] not in _reserved:
					allows1 = False
				i += 1

		except IndexError:
			print(f"{_cnBlueB}Error on line {j} on position {tabs+i}{_cnNull}")
			pass

		if head:
			html += head
			head  = ''

		allows1  = True
		html += '\n'

		j    += 1
		links = 0
		text  = file.readline()

	return html


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
		'output':          'Output.html',
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

Usage:{_cnNull}
	{_cnHlfb}${_cnNull+_cnBold} main.py <str> [option] (<str|int>)

Commands:{_cnNull}
	{_cnBold}-h{_cnNull}	Print this help.
	{_cnBold}-o   {_cnNull+_cnHlfb}…{_cnNull}	Give an output file.
	{_cnBold}-f   {_cnNull+_cnHlfb}…{_cnNull}	Give an output format.
	{_cnBold}-s   {_cnNull+_cnHlfb}…{_cnNull}	Give stylesheets.
	{_cnBold}-sb  {_cnNull+_cnHlfb}…{_cnNull}	Bundles stylesheet inside the output HTML.
	{_cnBold}-ds  {_cnNull+_cnHlfb}…{_cnNull}	Custom style sheet.
	{_cnBold}-dsb {_cnNull+_cnHlfb}…{_cnNull}	Bundle default stylesheet inside the output HTML.
	{_cnBold}-lds{_cnNull}	List all default styles.

For more information please read Syntax.mr:
{_cnNull+_cnHlfb}${_cnNull+_cnBold} main.py Syntax.mr -o Syntax.html{_cnNull}""")
	# {_cnBold}-lf{_cnNull}	List all formats


if __name__ == "__main__":
	import os

	for i in os.listdir('./stylesheets/'):
		if os.path.isfile(i) and i.endswith('.css') and len(i) > 4:
			_defStyleR.append(i[:-4])
	# print(_defStyleR)

	from sys import argv
	main(argv)
