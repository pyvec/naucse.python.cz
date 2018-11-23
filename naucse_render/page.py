from pathlib import Path

import jinja2

from .load import read_yaml
from .templates import environment, vars_functions
from .markdown import convert_markdown

def lesson_url(lesson_name, *, page='index'):
    if page == 'index':
        return f'naucse:lesson?lesson={lesson_name}'
    else:
        return f'naucse:lesson?lesson={lesson_name}&page={page}'


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

    text = env.get_template(page_name).render(
        lesson_url=lesson_url,
        subpage_url=lambda page: lesson_url(lesson_slug, page=page),
        **{'$solutions': solutions},
        **vars_functions(vars),
    )

    if info['style'] == 'md':
        text = convert_markdown(text)
    else:
        text = ''

    return {
        'content': text,
        'solutions': solutions,
        'source_file': path,
    }
