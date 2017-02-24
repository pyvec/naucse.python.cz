from jinja2 import Markup

from naucse.routes import app
from naucse import markdown_util


@app.template_filter('markdown')
def convert_markdown(text, inline=False):
    return markdown_util.convert_markdown(text, inline=inline)
