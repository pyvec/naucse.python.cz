from markdown import markdown
from textwrap import dedent
from jinja2 import Markup

from naucse.routes import app


@app.template_filter('markdown')
def convert_markdown(text, inline=False):
    text = dedent(text)
    result = Markup(markdown(text))

    # Markdown code blocks are translated literally, this solves problem with entities.
    result = result.replace('&amp;', '&').replace('&gt;', '>').replace('&#39;', "'").replace('&#34;', '"').replace('&lt;', '<')

    if inline and result.startswith('<p>') and result.endswith('</p>'):
        result = result[len('<p>'):-len('</p>')]

    return result
