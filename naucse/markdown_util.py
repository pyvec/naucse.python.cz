from textwrap import dedent

from markdown import Markdown
from markdown.extensions.admonition import AdmonitionExtension
from jinja2 import Markup

markdown = Markdown(
    extensions=[
        AdmonitionExtension(),
    ],
)

def convert_markdown(text, *, inline=False):
    text = dedent(text)
    result = Markup(markdown.convert(text))

    if inline and result.startswith('<p>') and result.endswith('</p>'):
        result = result[len('<p>'):-len('</p>')]

    return result
