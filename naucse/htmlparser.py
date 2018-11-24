from urllib.parse import urlsplit, urlunsplit, parse_qsl
import re

from jinja2 import Markup
import lxml.html
import lxml.etree

class DisallowedElement(Exception):
    pass

class DisallowedAttribute(DisallowedElement):
    pass

class DisallowedLink(DisallowedElement):
    pass

class DisallowedURLScheme(DisallowedLink):
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
}

def convert_link(attr_name, value, *, url_for=None):
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
    if url.scheme == 'naucse':
        if not url_for:
            raise DisallowedURLScheme(url.scheme)
        query = dict(parse_qsl(url.query))
        for name in query:
            if not re.match(r'^[-_a-z]+$', name):
                raise DisallowedLink(value)
        new_url = url_for[url.path](**query)
        if url.fragment:
            scheme, netloc, path, query, fragment = urlsplit(new_url)
            new_url = urlunsplit((scheme, netloc, path, query, url.fragment))
        return new_url
    else:
        raise DisallowedURLScheme(url.scheme)

    # Should not happen
    raise DisallowedLink(value)


def sanitize_element(element, *, url_for=None):
    if isinstance(element.tag, str):
        if element.tag not in ALLOWED_ELEMENTS:
            raise DisallowedElement(element.tag)
    elif element.tag is lxml.etree.Comment:
        pass
    else:
        raise DisallowedElement(element)

    for attr_name, value in list(element.items()):
        if attr_name == 'style':
            del element.attrib[attr_name]
            continue

        if (
            attr_name not in ALLOWED_ATTRIBUTES
            and attr_name not in PER_TAG_ATTRIBUTES.get(element.tag, ())
        ):
            raise DisallowedAttribute(f'{attr_name} on {element.tag}')

        if attr_name in {'href', 'src'}:
            element.attrib[attr_name] = convert_link(
                attr_name, value, url_for=url_for)

    for child in element:
        sanitize_element(child, url_for=url_for)


def sanitize_fragment(fragment, *, url_for=None):
    if isinstance(fragment, str):
        return Markup.escape(fragment)
    else:
        sanitize_element(fragment, url_for=url_for)
        return Markup(lxml.etree.tounicode(fragment, method='html'))


def sanitize_html(text, *, url_for=None):
    """Converts untrusted HTML to a naucse-specific form.

    Raises exceptions for potentially dangerous content.
    """

    fragments = [
        sanitize_fragment(fragment, url_for=url_for)
        for fragment in lxml.html.fragments_fromstring(text)
    ]

    return Markup().join(fragments)
