from xml.dom import SyntaxErr

from html.parser import HTMLParser

import cssutils


class DisallowedElement(Exception):
    pass


class InvalidHTML(DisallowedElement):
    pass


class DisallowedAttribute(DisallowedElement):
    pass


class DisallowedStyle(Exception):

    _BASE = "Style element or page css are only allowed when they modify .dataframe elements."
    COULD_NOT_PARSE = _BASE + " Ccould not parse the styles and verify."
    OUT_OF_SCOPE = _BASE + " Rendered page contains a style that modifies something else."


class AllowedElementsParser(HTMLParser):
    """
    This parser is used on all HTML returned from forked repositories.

    It raises exceptions in two cases:

    * :class:`DisallowedElement` - if a element not defined in :attr:`allowed_elements` is used
    * :class:`DisallowedStyle` - if a <style> element contains unparsable css or if it modifies something
      different than ``.dataframe`` elements.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.css_parser = cssutils.CSSParser(raiseExceptions=True)

        #: Set of allowed HTML elements
        #: It has been compiled out of elements currently used in canonical lessons
        self.allowed_elements = {
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

        #: Set of allowed HTML attributes
        #: Compiled out of currently used in canonical lesson
        self.allowed_attributes = {
            'alt', 'aria-hidden', 'border', 'class', 'color', 'colspan', 'controls', 'cx', 'cy', 'd', 'halign', 'href',
            'id', 'r', 'rowspan', 'src', 'start', 'title', 'type', 'valign', 'viewbox',

            # inline styles generated from notebook converter
            'style',
        }

        self.attrs = set()

    def error(self, message):
        raise InvalidHTML(message)

    def check_attributes(self, attrs):
        attr_names = set([x[0] for x in attrs])

        if len(attr_names - self.allowed_attributes):
            raise DisallowedAttribute("Attributes '{}' are not allowed".format(", ".join(attr_names)))

    def handle_starttag(self, tag, attrs):
        if tag not in self.allowed_elements:
            raise DisallowedElement(f"Element {tag} is not allowed.")

        self.check_attributes(attrs)

    def handle_startendtag(self, tag, attrs):
        if tag not in self.allowed_elements:
            raise DisallowedElement(f"Element {tag} is not allowed.")

        self.check_attributes(attrs)

    def handle_data(self, data):
        if self.lasttag == "style":
            self.validate_css(data)

    def reset_and_feed(self, data):
        self.reset()
        self.feed(data)

    def allow_selector(self, selector: str):
        if not selector.startswith(".dataframe "):
            return False

        return True

    def validate_css(self, data):
        try:
            parsed_css = self.css_parser.parseString(data)
        except SyntaxErr:
            raise DisallowedStyle(DisallowedStyle.COULD_NOT_PARSE)
        else:
            if len(parsed_css.cssRules) == 0:
                return

            if not all([self.allow_selector(selector.selectorText)
                        for rule in parsed_css.cssRules
                        for selector in rule.selectorList]):
                raise DisallowedStyle(DisallowedStyle.OUT_OF_SCOPE)
