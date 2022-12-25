=Version 1.3.1 - 2022-12-25=
# Markright

## Motivations

***Well*** this was suppose to be a school project, turns out you need to be at
least two. So oh well, imma finish this thingy here and then rewrite it in some
other language like C for terminal and probably Dart or something because Python
is a bit meh...

The goal of this little script is to write MarkDown document and convert them to
HTML, you can also add CSS files to customize your document a bit, and you will
also be able to create Wikis with a tool I'll make in the future. (perhaps)

I said MarkDown but there is a reason why this is called MarkRight, it's based
of MarkDown but there are a few tweaks here and there to make the parsing
easier. Most of the styles stay the same, ``*`` for *italic* ``**`` for **bold**
and so on... Block quotes change a bit to ``<<`` ending with ``>>`` this is much
much easier to work with, and also not far from how we quote in casual text.
Tables also, have their little tweaks here and there, actually there won't be
any *table* for say, The point is to use CSS grids, but HTML tables could still
be used; *=To see...=*

## Install

Installing is pretty straight forward, however, I'll later make an install
script to install it quicker, for now you will have to either rely on Git or
Github download.

1.	You will need [Python](#Python) to use this software, you should also
	install [Git](#Git) if it is not already installed on your system
1.	Download or clone the repo either downloading the zip file in Github
	(Code > Local > Download ZIP), unzip and use.

	Or with Git
	```sh
	git clone https://github.com/Vedqiibyol/MarkRight.git
	```
1.	Run the program with Python, see down bellow.

# Syntax

Something I need to do, when version 2 comes out.

# How to use and tasks ahead

Here are the following tasks ahead, and ToDos.

I very much suggest you use MarkRight to read this document:

```sh
main.py README.md -o README.html
```

- [-] Implementation
	- [x] Paragraphs
	- [-] Code blocks
	- [x] style
	- [x] heading
	- [x] a help manual
	- [-] document
		- [x] gen
		- [-] style
		- [-] script
	- [-] lists
		- [x] unordered lists, `ul`
		- [-] ordered lists, `ol`
			- [ ] list style
			- [x] start
		- [x] task lists, `tl`
		- [x] reference lists, `rl`
	- [ ] inline style change
	- [ ] more scripts for stuff.
	- [-] styles
	- [ ] tables ==New Syntax? Let me know if you have an idea!==
	- [-] content
		- [x] basic
		- [x] wikilink
		- [x] ext
	- [ ] wikilinks preview HTML
	- [ ] wikilinks preview MarkDown
	- [ ] Styles
		- [ ] `dragonik`
		- [ ] `textura`
		- [ ] `textura-dark`
		- [ ] `textura-light`

		- [ ] `dark-serif`
		- [ ] `dark-roboto`
		- [ ] `dark-roman`
		- [ ] `dark-mono`
		- [ ] `light-serif`
		- [ ] `light-roboto`
		- [ ] `light-roman`
		- [ ] `light-mono`

		- [ ] `dark-red-serif`
		- [ ] `dark-blue-serif`
		- [ ] `dark-green-serif`
		- [ ] `dark-purple-serif`
		- [ ] `dark-magenta-serif`
		- [ ] `dark-pink-serif`
		- [ ] `dark-cyan-serif`

		- [ ] `dark-red-roman`
		- [ ] `dark-blue-roman`
		- [ ] `dark-green-roman`
		- [ ] `dark-purple-roman`
		- [ ] `dark-magenta-roman`
		- [ ] `dark-pink-roman`
		- [ ] `dark-cyan-roman`

		- [ ] `dark-red-roboto`
		- [ ] `dark-blue-roboto`
		- [ ] `dark-green-roboto`
		- [ ] `dark-purple-roboto`
		- [ ] `dark-magenta-roboto`
		- [ ] `dark-pink-roboto`
		- [ ] `dark-cyan-roboto`

		- [ ] `dark-red-mono`
		- [ ] `dark-blue-mono`
		- [ ] `dark-green-mono`
		- [ ] `dark-purple-mono`
		- [ ] `dark-magenta-mono`
		- [ ] `dark-pink-mono`
		- [ ] `dark-cyan-mono`

		- [ ] `light-red-serif`
		- [ ] `light-blue-serif`
		- [ ] `light-green-serif`
		- [ ] `light-purple-serif`
		- [ ] `light-magenta-serif`
		- [ ] `light-pink-serif`
		- [ ] `light-cyan-serif`

		- [ ] `light-red-roboto`
		- [ ] `light-blue-roboto`
		- [ ] `light-green-roboto`
		- [ ] `light-purple-roboto`
		- [ ] `light-magenta-roboto`
		- [ ] `light-pink-roboto`
		- [ ] `light-cyan-roboto`

		- [ ] `light-red-roman`
		- [ ] `light-blue-roman`
		- [ ] `light-green-roman`
		- [ ] `light-purple-roman`
		- [ ] `light-magenta-roman`
		- [ ] `light-pink-roman`
		- [ ] `light-cyan-roman`

		- [ ] `light-red-mono`
		- [ ] `light-blue-mono`
		- [ ] `light-green-mono`
		- [ ] `light-purple-mono`
		- [ ] `light-magenta-mono`
		- [ ] `light-pink-mono`
		- [ ] `light-cyan-mono`

		- [ ] `dark-researchpaper`
		- [ ] `light-researchpaper`




# Links

[Python]: https://www.python.org/
[Git]: https://git-scm.com/download/win


