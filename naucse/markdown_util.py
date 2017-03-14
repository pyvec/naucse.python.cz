from textwrap import dedent
import re

import mistune
from jinja2 import Markup


class BlockGrammar(mistune.BlockGrammar):
    admonition = re.compile(r'^!!! *(\S+) *"([^"]*)"\n((\n| .*)+)')
    #admonition = re.compile(r'^!!!')


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
        #XXX: CodeHiliteExtension(guess_lang=False),
        #XXX: DefListExtension(),
    #],
)


def convert_markdown(text, *, inline=False):
    text = dedent(text)
    result = Markup(markdown(text))

    if inline and result.startswith('<p>') and result.endswith('</p>'):
        result = result[len('<p>'):-len('</p>')]

    return result
