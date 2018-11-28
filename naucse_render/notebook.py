from nbconvert import HTMLExporter
from nbconvert.filters.highlight import Highlight2HTML
import nbformat
import traitlets

from .markdown import convert_markdown


class NaucseHTMLExporter(HTMLExporter):
    def __init__(self, convert_url, *args, **kwargs):
        self._convert_url = convert_url
        super().__init__(*args, **kwargs)

    @traitlets.default('template_file')
    def _template_file_default(self):
        return 'basic'

    def from_notebook_node(self, nb, resources=None, **kw):
        '''So we could use our own template filters'''
        langinfo = nb.metadata.get('language_info', {})
        lexer = langinfo.get('pygments_lexer', langinfo.get('name', None))
        highlight = Highlight2HTML(pygments_lexer=lexer, parent=self)

        def convert_markdown_contexted(text):
            return convert_markdown(text, self._convert_url)

        self.register_filter('markdown2html', convert_markdown_contexted)
        self.register_filter('highlight_code', highlight)
        return super().from_notebook_node(nb, resources, **kw)


def convert_notebook(raw, convert_url=None):
    convert_url = convert_url if convert_url else lambda x: x
    notebook = nbformat.reads(raw, as_version=4)
    html_exporter = NaucseHTMLExporter(convert_url)
    body, resources = html_exporter.from_notebook_node(notebook)
    return body
