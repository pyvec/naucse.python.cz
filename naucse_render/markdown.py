from textwrap import dedent
import re

from ansi2html import Ansi2HTMLConverter
import mistune
from jinja2 import Markup
import pygments
import pygments.lexers
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Generic, Text, Comment
import pygments.formatters.html


ansi_convertor = Ansi2HTMLConverter(inline=True)

pygments_formatter = pygments.formatters.html.HtmlFormatter(
    cssclass='highlight'
)

_admonition_leading_pattern = re.compile(r'^ *> ?', flags=re.M)


class BlockGrammar(mistune.BlockGrammar):
    admonition = re.compile(r'^> *\[(\S+)\]([^\n]*)\n((>[^\n]*[\n]{0,1})*)')
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
            'title': m.group(2).strip(),
        })

        text = _admonition_leading_pattern.sub('', m.group(3))

        self.parse(dedent(text))
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


def style_space_after_prompt(html):
    return re.sub(r'<span class="gp">([^<]*[^<\s])</span>(\s)',
                  r'<span class="gp">\1\2</span>',
                  html)


def matrix_multiplication_operator(html):
    return html.replace('<span class="err">@</span>',
                        '<span class="o">@</span>')


class MSDOSSessionVenvLexer(RegexLexer):
    """Lexer for simplistic MSDOS sessions with optional venvs.

    Note that this doesn't use ``Name.Builtin`` (class="nb"), which naucse
    styles the same as the rest of the command.
    """
    name = 'MSDOS Venv Session'
    aliases = ['dosvenv']
    tokens = {
        'root': [
            (r'((?:\([_\w]+\))?\s?>\s?)([^#\n]*)(#.*)?',
             bygroups(Generic.Prompt, Text, Comment)),
            (r'(.+)', Generic.Output),
        ]
    }


def get_lexer_by_name(lang):
    """
    Workaround for our own lexer. Normally, new lexers have to be added trough
    entrypoints to be locatable by get_lexer_by_name().
    """
    if lang == 'dosvenv':
        return MSDOSSessionVenvLexer()
    return pygments.lexers.get_lexer_by_name(lang)


class Renderer(mistune.Renderer):
    code_tmpl = '<div class="highlight"><pre><code>{}</code></pre></div>'

    def __init__(self, convert_url, *args, **kwargs):
        self._convert_url = convert_url
        super().__init__(*args, **kwargs)

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
        lexer = get_lexer_by_name(lang)
        html = pygments.highlight(code, lexer, pygments_formatter).strip()
        html = style_space_after_prompt(html)
        if lang in ('python', 'pycon'):
            html = matrix_multiplication_operator(html)
        return html

    def deflist(self, items):
        tags = {'term': 'dt', 'def': 'dd'}
        return '<dl>\n{}</dl>'.format(''.join(
            '<{tag}>{text}</{tag}>'.format(tag=tags[type], text=text)
            for type, text in items
        ))

    def link(self, link, title, text):
        return super().link(self._convert_url(link), title, text)

    def image(self, src, title, text):
        return super().image(self._convert_url(src), title, text)


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


def convert_markdown(text, convert_url=None, *, inline=False):
    convert_url = convert_url if convert_url else lambda x: x

    text = dedent(text)

    markdown = Markdown(
        escape=False,
        block=BlockLexer(),
        renderer=Renderer(convert_url),
    )
    result = markdown(text).strip()

    if inline and result.startswith('<p>') and result.endswith('</p>'):
        result = result[len('<p>'):-len('</p>')]

    return Markup(result)
