from pathlib import Path

import mistune

from .load import read_yaml


def render_page(lesson_slug, page):
    lesson_directory = Path('lessons', lesson_slug)
    info = read_yaml(lesson_directory / 'info.yml')
    source = (lesson_directory / (page + '.md')).read_text(encoding='utf-8')
    return mistune.markdown(source)
