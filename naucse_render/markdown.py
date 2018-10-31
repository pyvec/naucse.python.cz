import mistune
from jinja2 import Markup


def convert_markdown(text, inline=False):
    result = mistune.markdown(text)

    if inline:
        if not (result.startswith('<p>') and result.endswith('</p>')):
            raise ValueError('Inline Markdown not a paragraph: ' + result)
        result = result[len('<p>'):-len('</p>')]

    return Markup(result)
