import textwrap

from jinja2 import Markup

from naucse.routes import app
from naucse import markdown_util


@app.template_filter('markdown')
def convert_markdown(text, inline=False):
    return markdown_util.convert_markdown(text, inline=inline)


@app.template_filter('dedent')
def dedent(text):
    return textwrap.dedent(text)


@app.template_filter('extract_part')
def extract_part(text, part, delimiter):
    """Extract the given part of text. Parts are delimited by `delimiter`.

    Indexing starts at zero.
    """
    return text.split(delimiter)[part]


@app.template_filter('solution')
def solution(text):
    """A solution to a problem.

    The intent is for the solution to be hidden by default, and only shown
    after an explicit action by the reader.
    """
    t = Markup(textwrap.dedent("""
        <div class="solution">
            <h3>Řešení</h3>
            <div class="solution-body">
                {}
            </div>
        </div>
    """))
    return t.format(markdown_util.convert_markdown(text))
