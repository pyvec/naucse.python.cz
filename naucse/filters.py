from markdown import markdown
from textwrap import dedent
from jinja2 import Markup

from naucse.routes import app


@app.template_filter('markdown')
def convert_markdown(text, inline=False):
    text = dedent(text)
    result = Markup(markdown(text))

    if inline and result.startswith('<p>') and result.endswith('</p>'):
        result = result[len('<p>'):-len('</p>')]

    return result


@app.template_filter('md_note')
def markdown_note(text):
    md_text = convert_markdown(text)
    return Markup('<p class="note">{}</p>').format(md_text)
