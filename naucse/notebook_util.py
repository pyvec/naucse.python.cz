from nbconvert import HTMLExporter
from nbconvert.filters.highlight import Highlight2HTML, _pygments_highlight
import nbformat
import traitlets
import pygments

from . markdown_util import convert_markdown


class Highlight2HTMLCodehilite(Highlight2HTML):
    '''We need to do all this just to add the codehilite cssclass'''
    def __call__(self, source, language=None, metadata=None):
        language = language or self.pygments_lexer
        formatter = pygments.formatters.HtmlFormatter(
            cssclass='codehilite highlight hl-'+language
        )
        return _pygments_highlight(source if len(source) > 0 else ' ',
                                   formatter, language, metadata)


class NaucseHTMLExporter(HTMLExporter):
    @traitlets.default('template_file')
    def _template_file_default(self):
        return 'basic'

    def from_notebook_node(self, nb, resources=None, **kw):
        '''So we could use our own template filters'''
        langinfo = nb.metadata.get('language_info', {})
        lexer = langinfo.get('pygments_lexer', langinfo.get('name', None))
        highlight = Highlight2HTMLCodehilite(pygments_lexer=lexer, parent=self)
        self.register_filter('highlight_code', highlight)
        self.register_filter('markdown2html', convert_markdown)
        return super(HTMLExporter,
                     self).from_notebook_node(nb, resources, **kw)


html_exporter = NaucseHTMLExporter()


def convert_notebook(raw):
    notebook = nbformat.reads(raw, as_version=4)
    body, resources = html_exporter.from_notebook_node(notebook)
    return body
