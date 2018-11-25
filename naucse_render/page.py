from pathlib import Path, PosixPath
from urllib.parse import urlparse

import jinja2

from .load import read_yaml
from .templates import environment, vars_functions
from .markdown import convert_markdown

def lesson_url(lesson_name, *, page='index'):
    if page == 'index':
        return f'naucse:lesson?lesson={lesson_name}'
    else:
        return f'naucse:lesson?lesson={lesson_name}&page={page}'


def static_url(filename):
    return f'naucse:static?filename={filename}'


def rewrite_relative_url(url, slug):
    parsed = urlparse(url)
    if parsed.scheme or parsed.hostname:
        return url

    parts = list(PosixPath(parsed.path).parts)

    if parts and parts[0] == 'static':
        return static_url('/'.join(parts[1:]))

    dotdots = 0
    while parts and parts[0] == '..':
        dotdots += 1
        del parts[0]

    if dotdots == 2:
        group, name = parts
        return lesson_url(f'{group}/{name}')
    elif dotdots == 1:
        group, name = slug.split('/')
        [name] = parts
        return lesson_url(f'{group}/{name}')

    if parsed.path.startswith('.'):
        raise ValueError(url)
    return url


def render_page(lesson_slug, page, vars=None):
    lesson_directory = Path('lessons', lesson_slug)
    env = environment.overlay(loader=jinja2.FileSystemLoader(str(lesson_directory)))
    if vars is None:
        vars = {}
    info = read_yaml(lesson_directory / 'info.yml')
    info = {**info, **info.get('pages', {}).get(page, {})}

    page_name = page + '.' + info['style']

    path = lesson_directory / page_name
    text = path.read_text(encoding='utf-8')

    solutions = []

    def page_markdown(text, **kwargs):
        return convert_markdown(
            text,
            convert_url=lambda u: rewrite_relative_url(u, lesson_slug),
            **kwargs,
        )

    text = env.get_template(page_name).render(
        lesson_url=lesson_url,
        subpage_url=lambda page: lesson_url(lesson_slug, page=page),
        static=static_url,
        **{'$solutions': solutions, '$markdown': page_markdown},
        **vars_functions(vars),
    )

    if info['style'] == 'md':
        text = page_markdown(text)
    else:
        text = ''

    result = {
        'content': text,
        'solutions': solutions,
        'source_file': path,
    }
    if 'css' in info:
        result['css'] = info['css']
    if 'latex' in info:
        result['modules'] = {'katex': '0.7.1'}
    return result
