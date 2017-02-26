from textwrap import dedent

from markdown import Markdown
from markdown.extensions.admonition import AdmonitionExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.def_list import DefListExtension
from jinja2 import Markup

markdown = Markdown(
    extensions=[
        AdmonitionExtension(),
        FencedCodeExtension(),
        CodeHiliteExtension(guess_lang=False),
        DefListExtension(),
    ],
)

def convert_markdown(text, *, inline=False):
    text = dedent(text)
    result = Markup(markdown.convert(text))

    if inline and result.startswith('<p>') and result.endswith('</p>'):
        result = result[len('<p>'):-len('</p>')]

    return result
