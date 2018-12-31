from urllib.parse import urlsplit, urlunsplit, parse_qsl
import re

from jinja2 import Markup
import lxml.html
import lxml.etree
import cssutils
import xml.dom

class ValidationError(Exception):
    pass

class DisallowedElement(ValidationError):
    pass

class DisallowedAttribute(ValidationError):
    pass

class DisallowedLink(DisallowedAttribute):
    pass

class DisallowedURLScheme(DisallowedAttribute):
    pass

class CSSSyntaxError(ValidationError):
    pass

ALLOWED_ELEMENTS = {
    # functional:
    'a', 'abbr', 'audio', 'img', 'source',

    # styling:
    'big', 'blockquote', 'code', 'font', 'i', 'tt', 'kbd', 'u', 'var', 'small', 'em', 'strong', 'sub',

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

    # A special check is applied in :meth:`handle_data` method
    # (only ``.dataframe`` styles allowed, generated from notebook converter)
    'style',
}

ALLOWED_ATTRIBUTES = {
    'class',
    'id',   # XXX: validate id's
    'aria-hidden',
}
PER_TAG_ATTRIBUTES = {
    'a': {'href'},
    'img': {'src', 'alt'},
    'font': {'color'},
    'ol': {'start'},
    'svg': {'viewbox'},
    'path': {'d'},
    'circle': {'cx', 'cy', 'r'},
    'audio': {'controls'},
    'source': {'src', 'type'},
    'table': {'border'},
    'td': {'rowspan', 'colspan', 'valign', 'halign'},
    'th': {'rowspan', 'colspan', 'valign', 'halign'},
}

def convert_link(attr_name, value, *, naucse_urls=None):
    url = urlsplit(value)
    if url.scheme in ('http', 'https'):
        if url.netloc == '':
            raise DisallowedLink(value)
        return urlunsplit(url)
    elif url.scheme == '':
        if url.netloc == '':
            # Relative URL
            if url.path.startswith('static/'):
                return url.path
            elif url.path != '':
                # Documents should not assume that naucse has any particular
                # URL structure, so links to other documents aren't allowed.
                raise DisallowedLink(value)
            if url.query:
                # Query arguments are ignored on a static site; disallow them
                raise DisallowedLink(value)
            return urlunsplit(url)
        else:
            return urlunsplit(url)
    elif url.scheme == 'naucse':
        if not naucse_urls:
            raise DisallowedURLScheme(url.scheme)
        query = dict(parse_qsl(url.query))
        for name in query:
            if not re.match(r'^[-_a-z]+$', name):
                raise DisallowedLink(value)
        new_url = naucse_urls[url.path](**query)
        if url.fragment:
            scheme, netloc, path, query, fragment = urlsplit(new_url)
            new_url = urlunsplit((scheme, netloc, path, query, url.fragment))
        return new_url
    elif url.scheme == 'data':
        # XXX: Disallow?
        return value
    else:
        raise DisallowedURLScheme(url.scheme)

    # Should not happen
    raise DisallowedLink(value)


def sanitize_css(css):
    """Return ``css`` limited just to the ``.lesson-content`` element.

    This doesn't protect against malicious input.
    """
    parser = cssutils.CSSParser(
        fetcher=lambda url: None, validate=True, raiseExceptions=True,
    )
    try:
        parsed_css = parser.parseString(css)
    except xml.dom.SyntaxErr as e:
        raise CSSSyntaxError() from e

    for rule in parsed_css.cssRules:
        for selector in rule.selectorList:
            # the space is important - there's a difference between for example
            # ``.lesson-content:hover`` and ``.lesson-content :hover``
            selector.selectorText = ".lesson-content " + selector.selectorText

    return parsed_css.cssText.decode("utf-8")


def sanitize_element(element, *, naucse_urls=None):
    if isinstance(element.tag, str):
        if element.tag == 'style':
            if len(element):
                raise DisallowedElement(list(element)[0])
            if element.text is None:
                element.text = ''
            element.text = sanitize_css(element.text)
        elif element.tag not in ALLOWED_ELEMENTS:
            raise DisallowedElement(element.tag)
    elif element.tag is lxml.etree.Comment:
        pass
    else:
        raise DisallowedElement(element)

    for attr_name, value in list(element.items()):
        if attr_name == 'style':
            # XXX: Sanitize attributes
            # del element.attrib[attr_name]
            continue

        if (
            attr_name not in ALLOWED_ATTRIBUTES
            and attr_name not in PER_TAG_ATTRIBUTES.get(element.tag, ())
        ):
            raise DisallowedAttribute(f'{attr_name} on {element.tag}')

        if attr_name in {'href', 'src'}:
            element.attrib[attr_name] = convert_link(
                attr_name, value, naucse_urls=naucse_urls)
        elif attr_name == 'scoped':
            # Non-standard, obsolete attribute; see:
            # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style#Deprecated_attributes
            # We scope CSS in <style> tags in the validator, so the "scoped"
            # attribute would break browsers that still honor it.
            del element.attrib[attr_name]

    # Recurse
    for child in element:
        sanitize_element(child, naucse_urls=naucse_urls)


def sanitize_fragment(fragment, *, naucse_urls=None):
    if isinstance(fragment, str):
        return Markup.escape(fragment)
    else:
        sanitize_element(fragment, naucse_urls=naucse_urls)
        return Markup(lxml.etree.tounicode(fragment, method='html'))


def sanitize_html(text, *, naucse_urls=None):
    """Converts untrusted HTML to a naucse-specific form.

    Raises exceptions for potentially dangerous content.
    """

    fragments = [
        sanitize_fragment(fragment, naucse_urls=naucse_urls)
        for fragment in lxml.html.fragments_fromstring(text)
    ]

    return Markup().join(fragments)
