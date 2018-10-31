from pathlib import Path

import jinja2

from .load import read_yaml
from .templates import environment, vars_functions
from .markdown import convert_markdown

def lesson_url(lesson_name, *, page='index'):
    if page == 'index':
        return f'../../../{lesson_name}/'
    else:
        return f'../../../{lesson_name}/{page}/'


def subpage_url(subpage_name):
    return f'./{subpage_name}/'


def render_page(lesson_slug, page):
    lesson_directory = Path('lessons', lesson_slug)
    env = environment.overlay(loader=jinja2.FileSystemLoader(str(lesson_directory)))
    vars = {}
    info = read_yaml(lesson_directory / 'info.yml')
    info = {**info, **info.get('pages', {}).get(page, {})}

    page_name = page + '.' + info['style']

    path = lesson_directory / page_name
    text = path.read_text(encoding='utf-8')

    text = env.get_template(page_name).render(
        lesson_url=lesson_url,
        subpage_url=subpage_url,
        **{'$solutions': [], **vars_functions(vars)},
    )
    if info['style'] == 'md':
        text = convert_markdown(text)

    return text
