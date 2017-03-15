from textwrap import dedent
import re

import mistune
from jinja2 import Markup
import pygments
import pygments.lexers
import pygments.formatters.html

pygments_formatter = pygments.formatters.html.HtmlFormatter(
    cssclass='codehilite'
)


class BlockGrammar(mistune.BlockGrammar):
    admonition = re.compile(r'^!!! *(\S+) *"([^"]*)"\n((\n| .*)+)')


class BlockLexer(mistune.BlockLexer):
    grammar_class = BlockGrammar

    default_rules = [
        'admonition',
    ] + mistune.BlockLexer.default_rules

    def parse_admonition(self, m):
        self.tokens.append({
            'type': 'admonition_start',
            'name': m.group(1),
            'title': m.group(2),
        })
        self.parse(dedent(m.group(3)))
        self.tokens.append({
            'type': 'admonition_end',
        })


class Renderer(mistune.Renderer):
    def admonition(self, name, content):
        return '<div class="admonition {}">{}</div>'.format(name, content)

    def block_code(self, code, lang):
        if lang is not None:
            lang = lang.strip()
        if not lang or lang == 'plain':
            escaped = mistune.escape(code)
            return '<div class="codehilite"><pre><code>{}</code></pre></div>'.format(escaped)
        lexer = pygments.lexers.get_lexer_by_name(lang)
        return pygments.highlight(code, lexer, pygments_formatter).strip()


class Markdown(mistune.Markdown):
    def output_admonition(self):
        name = self.token['name']
        body = self.renderer.placeholder()
        if self.token['title']:
            template = '<p class="admonition-title">{}</p>\n'
            body += template.format(self.token['title'])
        while self.pop()['type'] != 'admonition_end':
            body += self.tok()
        return self.renderer.admonition(name, body)


markdown = Markdown(
    escape = False,
    block = BlockLexer(),
    renderer = Renderer(),
    #extensions=[
        #XXX: DefListExtension(),
    #],
)


def convert_markdown(text, *, inline=False):
    text = dedent(text)
    result = Markup(markdown(text))

    if inline and result.startswith('<p>') and result.endswith('</p>'):
        result = result[len('<p>'):-len('</p>')]

    return result
