from xml.dom import SyntaxErr
from urllib.parse import urlparse, urlunparse
import re

import cssutils
from jinja2 import Markup
import lxml.html
import lxml.etree

class DisallowedHTML(Exception):
    pass

class DisallowedElement(DisallowedHTML):
    pass

class DisallowedAttribute(DisallowedHTML):
    pass

class DisallowedURLScheme(DisallowedHTML):
    pass

class DisallowedStyle(DisallowedHTML):
    pass

class BadStyleSyntax(DisallowedStyle):
    pass


ALLOWED_ELEMENTS = {
    # functional:
    'a', 'abbr', 'audio', 'img', 'source',

    # styling:
    'big', 'blockquote', 'code', 'font', 'i', 'tt', 'kbd', 'u', 'var',
    'small', 'em', 'strong', 'sub',

    # formatting:
    'br', 'div', 'hr', 'p', 'pre', 'span',

    # lists:
    'dd', 'dl', 'dt', 'li', 'ul', 'ol',

    # headers:
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',

    # tables:
    'table', 'tbody', 'td', 'th', 'thead', 'tr',

    # icons:
    'svg', 'circle', 'path',

    # For <style>, a special check is applied below
}

ALLOWED_ATTRIBUTES = {
    'class',
    'id',
    'title',
    'aria-hidden',
}
PER_TAG_ATTRIBUTES = {
    'a': {'href'},
    'img': {'src', 'alt'},
    'font': {'color'},
    'ol': {'start'},
    'audio': {'controls'},
    'source': {'src', 'type'},

    # Tables:
    'table': {'border'},
    'th': {'rowspan', 'colspan', 'valign', 'halign'},
    'td': {'rowspan', 'colspan', 'valign', 'halign'},

    # icons:
    'svg': {'viewbox'},
    'path': {'d'},
    'circle': {'cx', 'cy', 'r'},
}

def sanitize_link(attr_name, value):
    url = urlparse(value)
    if url.scheme not in ('http', 'https', 'data', ''):
        raise DisallowedURLScheme(url.scheme)

    return urlunparse(url)


def sanitize_css(data):
    parser = cssutils.CSSParser(raiseExceptions=True)
    try:
        parsed_css = parser.parseString(data)
    except SyntaxErr:
        raise BadStyleSyntax("Could not parse CSS")
    else:
        if len(parsed_css.cssRules) == 0:
            return ''

    for rule in parsed_css.cssRules:
        for selector in rule.selectorList:
            if not selector.selectorText.startswith('.dataframe '):
                raise DisallowedStyle(
                    "Style element or inline css may only modify .dataframe "
                    f"elements, got {data!r}."
                )

    return data


def sanitize_element(element):

    # Allow only known tags and comments
    if isinstance(element.tag, str):
        if element.tag == 'style':
            if len(element):
                raise DisallowedElement(list(element)[0])
            sanitize_css(element.text)
        elif element.tag not in ALLOWED_ELEMENTS:
            raise DisallowedElement(element.tag)
    elif element.tag is lxml.etree.Comment:
        pass
    else:
        raise DisallowedElement(element)

    # Allow only known attributes
    for attr_name, value in list(element.items()):
        if attr_name == 'style':
            # Allow inline styles
            # XXX: This is a potential security risk.
            pass
        elif (
            attr_name not in ALLOWED_ATTRIBUTES
            and attr_name not in PER_TAG_ATTRIBUTES.get(element.tag, ())
        ):
            raise DisallowedAttribute(f'{attr_name} on {element.tag}')

        if attr_name in {'href', 'src'}:
            element.attrib[attr_name] = sanitize_link(attr_name, value)

    # Recurse
    for child in element:
        sanitize_element(child)


def sanitize_html(text):
    """Converts untrusted HTML to a naucse-specific form.

    Raises exceptions for potentially dangerous content.
    """

    fragments = lxml.html.fragments_fromstring(text)

    for fragment in fragments:
        sanitize_element(fragment)

    return Markup().join(
        Markup(lxml.etree.tounicode(f, method='html')) for f in fragments
    )
