from textwrap import dedent
import re

from  ansi2html import Ansi2HTMLConverter
import mistune
from jinja2 import Markup
import pygments
import pygments.lexers
import pygments.formatters.html


ansi_convertor = Ansi2HTMLConverter(inline=True)

pygments_formatter = pygments.formatters.html.HtmlFormatter(
    cssclass='codehilite'
)


class BlockGrammar(mistune.BlockGrammar):
    admonition = re.compile(r'^!!! *(\S+) *"([^"]*)"\n((\n| .*)+)')
    deflist = re.compile(r'^(([^\n: ][^\n]*\n)+)((:( {0,3})[^\n]*\n)( \5[^\n]*\n|\n)+)')


class BlockLexer(mistune.BlockLexer):
    grammar_class = BlockGrammar

    default_rules = [
        'admonition',
        'deflist',
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

    def parse_deflist(self, m):
        self.tokens.append({
            'type': 'deflist_term_start',
        })
        self.parse(dedent(m.group(1)))
        self.tokens.append({
            'type': 'deflist_term_end',
        })
        self.tokens.append({
            'type': 'deflist_def_start',
        })
        self.parse(dedent(' ' + m.group(3)[1:]))
        self.tokens.append({
            'type': 'deflist_def_end',
        })


def ansi_convert(code):
    replaced = code.replace('\u241b', '\x1b')
    return ansi_convertor.convert(replaced, full=False)


class Renderer(mistune.Renderer):
    code_tmpl = '<div class="codehilite"><pre><code>{}</code></pre></div>'

    def admonition(self, name, content):
        return '<div class="admonition {}">{}</div>'.format(name, content)

    def block_code(self, code, lang):
        if lang is not None:
            lang = lang.strip()
        if not lang or lang == 'plain':
            escaped = mistune.escape(code)
            return self.code_tmpl.format(escaped)
        if lang == 'ansi':
            converted = ansi_convert(code)
            return self.code_tmpl.format(converted)
        lexer = pygments.lexers.get_lexer_by_name(lang)
        return pygments.highlight(code, lexer, pygments_formatter).strip()

    def deflist(self, items):
        tags = {'term': 'dt', 'def': 'dd'}
        return '<dl>\n{}</dl>'.format(''.join(
            '<{tag}>{text}</{tag}>'.format(tag=tags[type], text=text)
            for type, text in items
        ))


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

    def output_deflist_term(self):
        items = [['term', self.renderer.placeholder()]]
        while True:
            end_token = 'deflist_{}_end'.format(items[-1][0])
            while self.pop()['type'] not in (end_token, 'paragraph'):
                items[-1][1] += self.tok()
            if self.token['type'] == 'paragraph':
                if items[-1][0] == 'term':
                    items.append(['term', self.renderer.placeholder()])
                    items[-1][1] += self.token['text']
                else:
                    items[-1][1] += self.output_paragraph()
            elif self.peek()['type'] == 'deflist_term_start':
                self.pop()
                items.append(['term', self.renderer.placeholder()])
            elif self.peek()['type'] == 'deflist_def_start':
                self.pop()
                items.append(['def', self.renderer.placeholder()])
            else:
                break
        return self.renderer.deflist(items)


markdown = Markdown(
    escape = False,
    block = BlockLexer(),
    renderer = Renderer(),
)


def convert_markdown(text, *, inline=False):
    # Workaround for https://github.com/lepture/mistune/issues/125
    NBSP_REPLACER = '\uf8ff'
    text = text.replace('\N{NO-BREAK SPACE}', NBSP_REPLACER)

    text = dedent(text)
    result = Markup(markdown(text))

    if inline and result.startswith('<p>') and result.endswith('</p>'):
        result = result[len('<p>'):-len('</p>')]

    # Workaround for https://github.com/lepture/mistune/issues/125
    result = result.replace(NBSP_REPLACER, '\N{NO-BREAK SPACE}')
    return result
