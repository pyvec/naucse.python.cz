from pathlib import Path

import mistune
import jinja2

from .load import read_yaml
from .templates import environment, vars_functions


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
        lesson_url=lambda a: '',  # XXX
        subpage_url=lambda a: '',  # XXX
        **{'$solutions': [], **vars_functions(vars)},
    )
    if info['style'] == 'md':
        text = mistune.markdown(text)

    return text
