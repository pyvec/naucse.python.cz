from html.parser import HTMLParser
from io import StringIO
import types
import re

class ValidationError(ValueError):
    """HTML failed to validate"""

control_characters_re = re.compile('[\x00-\x09\x0B-\x0C\x0E-\x1F\x7F]')

HEADERS = 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
BLOCK_TO_INLINE = 'p', 'pre'
BLOCK_TO_BLOCK = 'div', 'blockquote'
SIMPLE_INLINE = 'code',
INLINE = 'a', 'span', 'strong', 'br', 'em', 'img', 'var', 'kbd', 'hr'
LIST = 'ul', 'ol'
LIST_ITEM = 'li',


def convert_html(text):
    """Converts untrusted HTML to a naucse-specific form"""

    result = StringIO()

    state = types.SimpleNamespace()
    state.states = [('block', 'html')]

    def handle_tag(tag, attrs, end=False):
        attrs = dict(attrs)
        st = state.states[-1][0]
        if st == 'block':
            if tag in HEADERS:
                state.states.append(('simple-inline', tag))
                return write_tag(tag, attrs)
            elif tag in BLOCK_TO_INLINE:
                state.states.append(('inline', tag))
                return write_tag(tag, attrs)
            elif tag in BLOCK_TO_BLOCK:
                state.states.append(('block', tag))
                return write_tag(tag, attrs)
            elif tag in LIST:
                state.states.append(('list', tag))
                return write_tag(tag, attrs)
            elif tag in SIMPLE_INLINE:
                state.states.append(('inline', tag))
                return write_tag(tag, attrs)
            elif tag in INLINE:
                state.states.append(('inline', tag))
                return write_tag(tag, attrs)
            else:
                raise ValidationError(f'unexpected {st} tag: {tag}')
        elif st == 'simple-inline':
            if tag in SIMPLE_INLINE:
                state.states.append(('simple-inline', tag))
                return write_tag(tag, attrs)
            else:
                raise ValidationError(f'unexpected {st} tag: {tag}')
        elif st == 'inline':
            if tag in INLINE:
                state.states.append(('inline', tag))
                return write_tag(tag, attrs)
            elif tag in SIMPLE_INLINE:
                state.states.append(('inline', tag))
                return write_tag(tag, attrs)
            raise ValidationError(f'unexpected {st} tag: {tag}, {parser.getpos()} {text.splitlines()[12:15]}')
        elif st == 'list':
            if tag in LIST_ITEM:
                state.states.append(('block', tag))
                return write_tag(tag, attrs)
            raise ValidationError(f'unexpected {st} tag: {tag}')
        else:
            raise ValidationError(f'bad internal state: {st}')
        # XXX attrs
        # XXX validation
        if end:
            result.write(' />')
            handle_endtag(tag)
        else:
            result.write('>')

    def handle_endtag(tag):
        prev = state.states.pop()[1]
        if prev in ('br', 'img'):
            return handle_endtag(tag)
        if tag != prev:
            raise ValidationError(f'unclosed tag: {prev}')

    def write_tag(tag, attrs):
        result.write(f'<{tag}')

    class Parser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            handle_tag(tag, attrs)

        def handle_endtag(self, tag):
            handle_endtag(tag)
            result.write(f'</{tag}>')

        def handle_startendtag(self, tag, attrs):
            return handle_tag(tag, attrs, end=True)

        def handle_data(self, data):
            result.write(data)

        def handle_comment(self, comment):
            result.write(f'<!-- {comment} -->')

        def handle_decl(self, decl):
            raise  # XXX

        def handle_pi(self, decl):
            raise  # XXX

        def unknown_decl(self, decl):
            raise  # XXX

    parser = Parser(convert_charrefs=True)
    parser.feed(text)

    result = result.getvalue()

    if control_characters_re.search(text):
        raise ValidationError("control characters found in HTML")

    return result
