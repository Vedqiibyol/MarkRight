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



def IsValid(data):
	pos   = 0

	for i in data:
		if i in " \t\n\r<[{()}]>.,/?:;'\"%$#@!^&*=+\\|`~":
			return pos
		pos += 1
	pos = -1
	return pos

def StrMatch(txt, pos, target):
	return txt[pos:pos+len(target)] == target

def LnPlusTab(tab):
	return "\n" + '\t' * tab

# def ParseControls(text, pos, ls) -> int:

# TODO: preview MarkRight
# def ParsePreview(text, pos):

# TODO: LaTeX section with ``$$  $$``
# def ParseLatex(text, pos):


def ParseQuoteStart(text, pos):
	count = 0
	inc   = 0
	qbr   = False

	while StrMatch(text, pos, '> '):
		count += 1
		inc   += 2
		pos   += 2

	if StrMatch(text, pos, '>\n'):
		count += 1
		inc   += 1
		qbr    = True

	return (count, inc, qbr)

# TODO: add in file linking, list, etc.
# TODO: list index
# DONE TODO: improve the Wikilink format with tags formating
# TODO: implement external application
def ParseSequence(text, pos, img, iframe):
	ret   = ''
	inc   = 0

	data = text[pos : pos+256]

	if   StrMatch(text, pos, '[['):				# wikilink
		data = data[2:data.find(']]')]
		inc  = len(data)+4

		try:
			if StrMatch(data, 0, 'youtube://'):
				param  = data.split(' ')
				src    = param[0][10:]
				width  = '560'
				height = '315'
				try:
					width  = param[1]
					height = param[1]
				except IndexError: pass

				ret = f"""<iframe width="{width}" height="{height}" src="https://www.youtube.com/embed/{src}"
title="YouTube video player" frameborder="0"
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>"""

				return (inc, ret)
		except IndexError: pass

		if img: ret = f"<img src='{data}' alt='{data}'>"
		elif iframe:
			param  = data.split(' ')
			src    = param[0]
			width  = '560'
			height = '315'
			ret = f"<iframe src='{src}' alt='{src}' width='{width}' height='{height}'>"
		else: ret = f"<a href='{data}'>{data}</a>"

	elif StrMatch(text, pos, '['):				# markdown-style list (or image) text
		data = data[1:data.find(']')]
		inc  = len(data)+2

		pos += inc

		# then markdown-style list (or image) src
		src = text[pos : pos+256].strip()

		src = src[1:src.find(')')]
		inc += len(src)+2

		if img: ret = f"<img src='{src}' alt='{data}'>"
		else: ret = f"<a href='{src}'>{data}</a>"

	return (inc, ret)


def ParseTag(text, pos):
	valid = True
	ret   = ''

	txt = text[pos:256]

	end = IsValid(txt[1:])
	txt = txt[:end+1]
	tag = txt[1:]

	if end == -1: valid = False
	if len(tag) == 0: valid = False


	ret = f"<span id='{tag}' class='tag'>{txt}</span>"

	return (valid, len(txt), ret)

# DONE TODO: implement tag system
def ParseHead(text, pos):
	valid = False
	inc   = 0
	reth  = ''

	data = text[pos:pos+256].split(' ', 1)[0]

	if StrMatch(text, pos, '#.'):
		reth = 'hsmall'

		inc = 2
	else:
		for i in data:
			if i != '#' and inc < 6: break
			inc += 1

		if inc:
			reth = f"h{str(inc)}"

	if inc == len(data):
		valid = True

	return (valid, inc+1, reth)


def AddStyle(style, styles) -> str:
	styles[style] ^= 1

	#ls[-1] += f"<{'/' * styles[style]}{style}>"

	return f"<{'/' * (not styles[style])}{style}>"

# TODO: perhaps make it a bit faster with a function a bit more useful
# TODO: Add the styling properties for code with '¬'
# TODO: and the character ignore, '\'
def ParseStyle(text, pos, styles):
	inc   = 0
	valid = False
	ret   = ''
	# if ch == '\\' or (ch == '¬' and code == True):
	#	pass

	if   StrMatch(text, pos, '**'):  ret = AddStyle('strong', styles); inc = 2; valid = True
	elif StrMatch(text, pos, '=='):  ret = AddStyle('mark',   styles); inc = 2; valid = True
	elif StrMatch(text, pos, '__'):  ret = AddStyle('ins',    styles); inc = 2; valid = True
	elif StrMatch(text, pos, '~~'):  ret = AddStyle('strike', styles); inc = 2; valid = True
	elif StrMatch(text, pos, '*'):   ret = AddStyle('em',     styles); inc = 1; valid = True
	elif StrMatch(text, pos, '='):   ret = AddStyle('half',   styles); inc = 1; valid = True
	elif StrMatch(text, pos, '_'):   ret = AddStyle('sub',    styles); inc = 1; valid = True
	elif StrMatch(text, pos, '`'):   ret = AddStyle('code',   styles); inc = 1; valid = True
	elif StrMatch(text, pos, '^'):   ret = AddStyle('sup',    styles); inc = 1; valid = True

	return (valid, inc, ret)



def Parse(path):
	file = open(path)
	text = file.read(0x10000)

	# This list should later be changed to a single string, or just a buffer
	# class, that will flush it's content into the output.
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

	# * Booleans
	forcecode  = False   # The ``Forcecode`` flag, just like the
	                     # simpler backticks, produces an output with
	                     # the `<code>` tag, but the forcecode does not parse
	                     # for styles in between it's range.
	blockquote = False   # Blockquotes are already present in HTML, `<blockquote>` or `<q>`.
	                     # But with the MarkDown syntax, which MarkRight is based on
	                     # it's behaviour is trickier for the purposes of readability,
	                     # thus a flag is needed along with a series of checks.

	# These variable count the number of tabs, spaces before a non-white space character.
	tab        = 0
	spc        = 0

	# This stores the head string (h1, h2, etc.).
	head       = ''
	quote      = 0

	# store the list type in the list, the index is the depth
	# a tuple, with first position, the type, second the tabs as depth.
	# | type       | tab count     |
	# | --- | ---- | ------------- |
	# | 0   | ul   | integer       |
	# | 1   | ol   | storing the   |
	# | 2   | task | lists's depth |
	# it's a a stack, pop and append, and there is no boiler plate needed,
	# Python's lists work fine.
	lists = []


	lnbefore    = 0       # Counts the number of new line before a non-white space character
	                      # is encountered.
	tabsbefore  = 0       # Same, with tabs; can be used for lists.
	spacebefore = 0       # Same, with spaces; can also be used for lists, or code blocks.

	headbefore  = 0

	# * Flags
	allowshead  = False   # This flag tells if the parser is allowed to add a heading tag or not.
	allowsquote = False   # Same, for blockquote tags.
	inlist      = False   # This tells the Parser if it is currently parsing a list or not;
	                      # this flag is very important regarding the two other flags here-above.


	# ! debug
	# lncnt = 0
	# lnchr = 0


	while i < len(text):
		# ! debug
		# if text[i] == '\n':
		# 	lncnt += 1
		# 	print(f"\x1B[41mLine № {lncnt}\x1B[0m")
		# 	lnchr = 0

		prevbr = False

		# * Checks

		# TODO: something for <br>s in blockquotes
		if       text[i] == '\n':              lnbefore    += 1 # line breaks until non-whitespaces characters
		if       text[i] == '\t':              tabsbefore  += 1 # same with tabs
		if       text[i] == ' ' and lnbefore:  spacebefore += 1 # nifty thing, just there

		# Headings check, boolean
		# TODO

		# Blockquotes check, boolean
		# TODO

		try:
			if headbefore:
				headbefore -= 1
			elif lnbefore and not head and not quote:
				html  += '<br>\n'
				i     += 1
				# prevbr = True


			# TODO: figure out if that's actually necessary
			# if text[i] == '\t':
			#	tab += 1
			#	i   += 1
			#	continue # along with the br stuff

			# TODO: same, is it necessary?
			# if text[i] == ' ' and prevbr:
			#	spc += 1
			#	i   += 1
			#	continue # welp, this is just better for compression.

			if StrMatch(text, i, '``'):
				forcecode ^= 1
				i         += 2
				html      += f"<{'/'*(not forcecode)}code>"

			# TODO: remove this tabulation, somehow
			if not forcecode:
				# doing the styles
				valid, inc, ret = ParseStyle(text, i, styles)

				if valid:
					i    += inc
					html += ret

				if StrMatch(text, i, '---'): # It's hard to make simpler.
					html += '<hr>'
					i    += 3
					# continue


				# TODO: refactor so you can have them in lists too
				# headers and header's tags
				# ---
				# 1. identify header, store, inc, etc.
				if text[i] == '#':
					# TODO: we have a code redonduncy, let's find a way to get rid of it
					if i == 0 or lnbefore:
						valid, inc, head = ParseHead(text, i)

						if valid:
							i    += inc
							html += f'<{head}>'

						# Maybe it's a tag after all...
						else:
							valid, inc, ret = ParseTag(text, i)

							if valid:
								i    += inc
								html += ret

								head  = ''
					else:
						valid, inc, ret = ParseTag(text, i)

						if valid:
							i    += inc
							html += ret

				# 2. detect end and add closing tag
				if head and text[i] == '\n':
					html      += f'</{head}>\n'
					head       = ''
					headbefore = 2
					continue


				# TODO:  refactor, you need to able to nest
				# TODO: blockquotes inside blockquotes
				# blockquotes
				# if we have ``> ``, that's one blockquote
				# recursive check, if a blockquote is in a blockquote, then we have ``> > ``
				# just count the number of ``> ``
				# Do not forget to have a flag
				# ╭──────────┬─────────────────────────╮
				# │> stuff   │ <- One blockquote       │
				# │> ssssss  │                         │
				# │          │                         │
				# │> RAWR!   │ <- another blockquote!  │
				# ╰──────────┴─────────────────────────╯
				# SO WE COUNT!
				# It's ~~list time!~~ INTEGER TIME!
				# © Comments by Vedqiibyol, 2022-10-31, I love them. NO TOUCHIE! HISSSSSSSSSSSSSSSSS!!!

				# count the number of following '> ' until line break
				# when it's different from quote:
				#   if inferior, add ``</blockquote>``
				#   if superior, add ``<blockquote>``
				# if none, quote = 0
				# only when we have a new line, so we can use `lnbefore`

				if lnbefore:
					count, inc, qbr = ParseQuoteStart(text, i)

					if count:
						print(count, inc, '|||', text[i:i+12])
						i += inc

						if count > quote:
							# TODO: handle custom styling for later, not important right now
							html += '<blockquote>\n' * (count - quote)
						else: # count < quote
							html += '</blockquote>\n' * (quote - count)

						quote = count
						inc   = 0

					#elif lnbefore > 1 and quote:
					elif lnbefore > 1:
						html += '</blockquote>\n' * quote
						# quote = 0
					if qbr:
						html += '<br>'
						qbr   = False




				# TODO: nothing, it's clean it's nice, but just check after.
				# sequences and markdown links
				if text[i] == '[':
					inc, ret = ParseSequence(text, i, False, False)

					i    += inc
					html += ret

				# images
				if StrMatch(text, i, '!['):
					inc, ret = ParseSequence(text, i+1, True, False)

					i    += inc + 1
					html += ret

				# preview, for wikis in particular
				if StrMatch(text, i, '?['):
					inc, ret = ParseSequence(text, i+1, False, True)

					i    += inc + 1
					html += ret




				# TODO: lists
				# Is it a list?
				# - detect start
				#   - digit            = <ol>
				#   - ``in "-+*"``     = <ul>
				#   - ``- [ ]``        = <fieldset class='task-list'>
				#   - number of tabs, EOL
				# - Always store the list started, we want a good syntax.
				# - when we encounter a big line break, we stop close the list
				# - when we encounter a list thingy starter, we close the <li>
				#   and we add another one, if we are sure to have another one,
				#   so we have a flag
				# ---
				# Our flags are:
				# - `lstype`, you know
				# - `lsstart`, you also know
				# - `hasended`, optional, we can just add ``</li></ol|ul>`` or ``</fieldset>``
				#   when we're done
				# - `lsdepth`, optional, but still good to have, we'll see

				# it needs to be a new line
				#if prevbr:
				#	# 1. Detecting the start
				#	#    - setting the flag of lists in the function for <br>s.
				#	# ---
				#	# ul
				#	if text[i] in '-+*':
				#		# 0 == ul
				#		if len(lists) == 0 or lists[-1][0] != 0 or lists[-1][1] != tab:
				#			lists.append([0, tab])
				#			html += '<ul>'
				#		else:
				#			html += '</li>'
				#		html += '<li>'
				#	# ol
				#	# TODO: make a function for the if-statement
				#	elif text[i].isdigit() and text[i+1] == '.' and text[i+2].isspace():
				#		# 1 == ol
				#		if len(lists) == 0 or lists[-1][0] != 1 or lists[-1][1] != tab:
				#			lists.append([1, tab])
				#			html += '<ol>'
				#		else:
				#			html += '</li>'
				#		html += '<li>'
				#
				#	"""# task-list, fieldset x input
				#	elif StrMatch(text, i, '- ['):
				#		#    x: checked
				#		#    o: indetermined
				#		# _SPC: uncked
				#		if len(lists) == 0 or lists[-1][0] != 2 or lists[-1][1] != tab:
				#			lists.append([2, tab])
				#			ls.append(f"<fieldset class='task-list'>")
				#		# TODO: add the task, as an <input>, and a <label>
				#		# TODO: have a generator the names
				#		else: ls.append("<li>")"""



			# else: # TODO: else or continue magic; the ultimate question
			#	# add characters


			# if text[i] != '\t': tab = 0
			# bleh, we never know
		except IndexError:
			break

		if not text[i].isspace():
			lnbefore    = 0
			tabsbefore  = 0
			spacebefore = 0


		html  += text[i]

		i     += 1
		prevbr = False
		tab    = 0



		# ! debug
		# lnchr += 1
		# print(f"\x1B[42m{lnchr}\x1B[0m ", end='')
	return html






def main(args):
	input      = ''
	output     = 'Output.mr'
	format     = 0 # 0: HTML, 1: PDF, 2: SVG, 3: PNG, 4: EPUB
	stylesheet = None

	if len(args) < 2:
		print("MarkRight requieres at least 1 arguement")
		print("Use -h if you need help")
		return -1

	i = 1
	while i < len(args):
		if args[i][0] == '-':
			match args[i][1:]:
				case 'h':
					Parse("./Syntax.me", format, True)
				case 'o':
					if i < len(args)-1:
						output = args[i+1]
						i += 1
					else:
						print("MarkRight requires one more arguements after '-o'")


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
