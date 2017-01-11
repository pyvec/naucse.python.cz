from markdown import markdown
from textwrap import dedent
from jinja2 import Markup

from routes import app


# Markdown is working.
@app.template_filter('markdown')
def convert_markdown(text):
    text = dedent(text)
    result = Markup(markdown(text))

    # Markdown code blocks are translated literally, this solves problem with entities.
    result = result.replace('&amp;', '&').replace('&gt;', '>').replace('&#39;', "'").replace('&#34;', '"').replace('&lt;', '<')
    
    return result
