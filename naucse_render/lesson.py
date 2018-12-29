"""
Retreive per-lesson meta-information

Reads source YAML files and merges them to one JSON, with
render info for items.
"""

from pathlib import Path
import datetime
import textwrap

import jsonschema

from .load import read_yaml
from .page import render_page


def get_lessons(lesson_slugs, vars=None, path='.'):
    path = Path(path).resolve()
    data = {}
    for slug in lesson_slugs:
        try:
            lesson_data = get_lesson(slug, vars, path)
        except FileNotFoundError:
            pass
        else:
            data[slug] = lesson_data
    return {
        'api_version': [0, 0],
        'data': data,
    }


def get_lesson(lesson_slug, vars, base_path):
    lesson_path = base_path / 'lessons' / lesson_slug
    lesson_info = read_yaml(base_path, 'lessons', lesson_slug, 'info.yml')

    lesson = {
        'title': lesson_info['title'],
        'static_files': dict(get_static_files(base_path, lesson_path)),
        'pages': {},
        'source_file': str(lesson_path / 'info.yml'),
    }

    lesson_vars = lesson_info.pop('vars', {})

    pages_info = lesson_info.pop('subpages', {})
    pages_info.setdefault('index', {})

    for slug, page_info in pages_info.items():
        info = {**lesson_info, **page_info}
        lesson['pages'][slug] = render_page(
            lesson_slug, slug, info, vars={**vars, **lesson_vars},
            path=base_path,
        )
    return lesson


def get_static_files(base_path, lesson_path):
    static_path = lesson_path / 'static'
    for file_path in static_path.glob('**/*'):
        if file_path.is_file():
            filename = str(file_path.relative_to(static_path))
            path = str(file_path.relative_to(base_path))
            yield (
                filename,
                {'path': path},
            )
