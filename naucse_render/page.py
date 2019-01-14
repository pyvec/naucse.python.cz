from pathlib import Path, PosixPath
from urllib.parse import urlparse
import types
import sys

import jinja2

from .templates import environment, vars_functions
from .markdown import convert_markdown
from .notebook import convert_notebook


def to_list(value):
    if isinstance(value, str):
        return [value]
    return value


def to_html_list(value, inline=False):
    return [convert_markdown(item, inline=inline) for item in to_list(value)]


def lesson_url(lesson_name, *, page='index', _anchor=''):
    url = f'naucse:page?lesson={lesson_name}'
    if page != 'index':
        url += f'&page={page}'
    if _anchor:
        url += f'#{_anchor}'
    return url


def static_url(filename, *, _anchor=''):
    url = f'naucse:static?filename={filename}'
    if _anchor:
        url += f'#{_anchor}'
    return url


def rewrite_relative_url(url, slug):
    """Rewrite relative URL in a page to lesson_url()/static_url()
    """
    parsed = urlparse(url)
    if parsed.scheme or parsed.hostname:
        return url

    parts = list(PosixPath(parsed.path).parts)

    if parts and parts[0] == 'static':
        return static_url('/'.join(parts[1:]), _anchor=parsed.fragment)

    dotdots = 0
    while parts and parts[0] == '..':
        dotdots += 1
        del parts[0]

    if dotdots == 2:
        group, name = parts
        return lesson_url(f'{group}/{name}', _anchor=parsed.fragment)
    elif dotdots == 1:
        group, name = slug.split('/')
        [name] = parts
        return lesson_url(f'{group}/{name}', _anchor=parsed.fragment)

    if parsed.path.startswith('.'):
        raise ValueError(url)
    return url


def render_page(lesson_slug, page_slug, info, path, vars=None):
    """Get rendered content and metainformation on one lesson page.
    """

    base_path = Path(path).resolve()

    print(f'Rendering page {lesson_slug} ({page_slug})', file=sys.stderr)
    if vars is None:
        vars = {}

    lessons_path = base_path / 'lessons'
    lesson_path = lessons_path / lesson_slug

    page = {
        'title': info['title'],
        'attribution': to_html_list(info['attribution'], inline=True),
        'license': info['license'],
        'slug': page_slug,
        'vars': {**vars, **info.get('vars', {})},
    }
    if 'license_code' in info:
        page['license_code'] = info['license_code']

    # Page content can be read from Markdown (md) or Jupyter Notebook (ipynb),
    # selected by 'style'.
    # Each is pre-processed by jinja2 by default (opt out with 'jinja': False).

    page_filename = page_slug + '.' + info['style']

    # List of solutions, filled in Jinja render step bellow
    solutions = []

    # Helpers for conferting URLs to naucse: links in Markdown
    def convert_page_url(url):
        return rewrite_relative_url(url, lesson_slug)

    def page_markdown(text, **kwargs):
        return convert_markdown(
            text,
            convert_url=convert_page_url,
            **kwargs,
        )

    # Jinja pre-processing
    page_path = lesson_path / page_filename
    if info.get('jinja', True):
        # Use a Jinja environment to enable includes/template inheritance
        env = environment.overlay(
            loader=jinja2.FileSystemLoader(str(lessons_path)),
        )
        text = env.get_template(f'{lesson_slug}/{page_filename}').render(
            lesson_url=lesson_url,
            subpage_url=lambda page: lesson_url(lesson_slug, page=page),
            static=static_url,

            # Special variables for internal use in filters
            **{'$solutions': solutions, '$markdown': page_markdown},

            # Helpers for render-specific variables (like user gender,
            # origin repo URL, presenter name)
            **vars_functions(vars),

            # XXX: 'lesson' for templates is deprecated
            lesson=types.SimpleNamespace(slug=lesson_slug),
        )
    else:
        text = page_path.read_text(encoding='utf-8')

    # Render from input format
    if info['style'] == 'md':
        text = page_markdown(text)
    elif info['style'] == 'ipynb':
        text = convert_notebook(text, convert_url=convert_page_url)
    else:
        raise ValueError(info['style'])

    # Auxilliary metadata
    page['content'] = text
    page['solutions'] = [{'content': s} for s in solutions]
    page['source_file'] = str(page_path.relative_to(base_path))
    if 'css' in info:
        page['css'] = info['css']
    if 'latex' in info:
        page['modules'] = {'katex': '0.7.1'}

    return page
