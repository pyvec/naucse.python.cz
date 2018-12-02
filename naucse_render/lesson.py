"""
Retreive course meta-information

Reads source YAML files and merges them to one JSON, with
render info for items.
"""

from pathlib import Path
import datetime
import textwrap

import jsonschema

from .load import read_yaml
from .page import render_page


def get_lessons(lesson_slugs, vars=None):
    return {slug: get_lesson(slug, vars) for slug in lesson_slugs}


def get_lesson(lesson_slug, vars):
    lesson_path = Path('lessons', lesson_slug)
    lesson_info = read_yaml('lessons', lesson_slug, 'info.yml')

    lesson = {
        'slug': lesson_slug,
        'title': lesson_info['title'],
        'static_files': dict(get_static_files(lesson_path)),
        'pages': {},
        'source_file': lesson_path / 'info.yml',
    }

    lesson_vars = lesson_info.pop('vars', {})

    pages_info = lesson_info.pop('subpages', {})
    pages_info.setdefault('index', {})

    for slug, page_info in pages_info.items():
        info = {**lesson_info, **page_info}
        lesson['pages'][slug] = render_page(
            lesson_slug, slug, info, vars={**vars, **lesson_vars}
        )

    return lesson


def get_static_files(path):
    static_path = path / 'static'
    for file_path in static_path.glob('**/*'):
        if file_path.is_file():
            filename = str(file_path.relative_to(static_path))
            path = str(file_path.relative_to('.'))
            yield (
                filename,
                {'filename': filename, 'path': path},
            )
