# Markright

# ONCE AGAIN!

I've decided, that, I would improve and entirely rewrite Markright, has I had
previously said, since I've modified Markright quite a bit in order to build my
website (it's still in progress btw c:), that I would add those modifications
and new features to the official thing! I also wanted to try out something else
than Python, because although I like tiss thing, it works, but not as well as
I'd like it to, and I can't manage to have a somewhat readable and digestible
code (at least in my opinion, and it might also be because I didn't quite use
the right technics but *details*). So, here it is, being rewritten in Swift!

# What has changed?

I've decided to make the tool easier to improve on, and add a few things that
will be great to make websites! You can easily add a header to your output HTML,
as well as a footer, an email form as, well, and pretty much anything with
snippets, and now also annotations!

Tables too will change from Markdown, to
something more flexible, and powerful (with merged cells, yeeeeeeeess~!).

I've decided to not change so much things from markdown, because after all, they
were quite good already and not everything has to change, I also modified the
style syntax in order to avoid all the potential conflict (and abuse of the
force-code feature - **Which I removed by the way**).

I'm also working a bit on
lists, I want to make them easier to use, and I am taking a bit of inspirations
from ASCIIDOC, but I am still not entirely sure, so stick with Markdown-style
lists for now...

I've also decided to change how paragraphs and line breaks will work, to make it
more semantically logic, let's say.

# Installing

Since it's Swift, there is nothing BUT the executable to download, which is
great!

You can download the executable from your platform through the installation
scripts in the release section, otherwise from `scripts/` or with the links at
the [bottom](#bottom) of the page.

Then simply execute the script, the
executable will be installed in the proper place from what you chose (system or
user), and added to the `PATH` variable.

\n
You may also want to download the core `markright.css` and `markright.js`
if you want to modify them, they are not required to run the executable
(because built-in) but they may be a good foundation to create your own
stylesheet.

# Usage

Simply run it from your shell,
```
mr
```

and
```
mr -?
```
to get help. Simple as that.

# Building

## Swift

Download Swift for your platform at [](https://www.swift.org/install/) and
install it.

There is nothing but Swift to download, it should download the
dependencies by itself.

## Markright

Clone it in a directory or download the Zip file in "Code" (the green button).

```
git clone https://github.com/Vedqiibyol/MarkRight.git
```

## Running and installing

```
swift run markright
swift build
```
