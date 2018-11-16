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
from .markdown import convert_markdown


API_VERSION = 1


def to_list(value):
    if isinstance(value, str):
        return [value]
    return value


def to_html_list(value, inline=False):
    return [convert_markdown(item, inline=inline) for item in to_list(value)]


def encode_dates(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    elif isinstance(value, dict):
        return {k: encode_dates(v) for k, v in value.items()}
    elif isinstance(value, (list, tuple)):
        return [encode_dates(v) for v in value]
    elif isinstance(value, (str, int, bool, type(None))):
        return value
    raise TypeError(value)


# XXX: Clarify the version

def get_course(course_slug: str, *, version: int) -> dict:
    """Get information about the course as a JSON-compatible dict"""

    if version <= 0:
        raise ValueError(f'Version {version} is not supported')

    if course_slug == 'lessons':
        info = get_canonical_lessons_info()
    else:
        parts = course_slug.split('/')
        if len(parts) == 1 or (len(parts) == 2 and parts[0] == 'courses'):
            info = read_yaml('courses', parts[-1], 'info.yml')
        elif len(parts) == 2:
            info = read_yaml('runs', *parts, 'info.yml')
        else:
            raise ValueError(f'Invalid course slug')

    info['api_version'] = 1, 1

    # XXX: Do we need these?
    info.pop('meta', None)
    info.pop('canonical', None)

    base_slug = info.pop('derives', None)
    if base_slug:
        base_course = read_yaml('courses', base_slug, 'info.yml')
    else:
        base_course = {}

    # Rename "plan" to "sessions"
    for d in info, base_course:
        if 'plan' in d:
            d['sessions'] = d.pop('plan')

    for session in info['sessions']:
        base = session.pop('base', None)
        if base:
            for base_session in base_course['sessions']:
                if base_session['slug'] == base:
                    break
            else:
                raise ValueError(f'Session {session} not found in base course')
            session.update(merge_dict(base_session, session))
        for material in session['materials']:
            lesson_slug = material.pop('lesson', None)
            if lesson_slug:
                update_lesson(material, lesson_slug, vars=info.get('vars', {}))
                if material.pop('url', None):
                    raise ValueError(f'Material {material} has URL')
                material.setdefault('type', 'lesson')
            else:
                url = material.pop('url', None)
                if url:
                    material['external_url'] = url
                    material.setdefault('type', 'link')
                else:
                    material.setdefault('type', 'special')

    result = encode_dates(info)
    schema = read_yaml('schema/fork-schema.yml')
    jsonschema.validate(result, schema)
    return result


def update_lesson(material, lesson_slug, vars):
    lesson_info = read_yaml('lessons', lesson_slug, 'info.yml')

    pages = lesson_info.pop('subpages', {})
    pages.setdefault('index', {})

    material_vars = material.pop('vars', None)

    for slug, page_info in pages.items():
        info = {**lesson_info, **page_info}
        page = {
            'title': info['title'],
            'attribution': to_html_list(info['attribution'], inline=True),
            'license': info['license'],
            'slug': slug,
            'render_call': {
                'entrypoint': 'naucse_render:render_page',
                'args': [lesson_slug, slug],
            }
        }
        if 'license_code' in info:
            page['license_code'] = info['license_code']
        if material_vars:
            page['vars'] = {**page.get('vars', {}), **material_vars}
        pages[page['slug']] = page

    material['pages'] = pages
    material['slug'] = lesson_slug
    material.setdefault('title', lesson_info['title'])

    # XXX: File edit path
    # XXX: Coverpages
    # XXX: Render Markdown/Validate HTML!

    # Afterwards:
    # XXX: date
    # XXX: start_time
    # XXX: end_time
    # XXX: has_irregular_time
    # XXX: prev/next

def merge_dict(base, patch):
    """Recursively merge `patch` into `base`

    If a key exists in both `base` and `patch`, then:
    - if the values are dicts, they are merged recursively
    - if the values are lists, the value from `patch` is used,
      but if the string `'+merge'` occurs in the list, it is replaced
      with the value from `base`.
    """

    result = dict(base)

    for key, value in patch.items():
        if key not in result:
            result[key] = value
            continue

        previous = base[key]
        if isinstance(value, dict):
            result[key] = merge_dict(previous, value)
        elif isinstance(value, list):
            result[key] = new = []
            for item in value:
                if item == '+merge':
                    new.extend(previous)
                else:
                    new.append(item)
        else:
            result[key] = value
    return result


def get_canonical_lessons_info():
    # XXX: Should this be here?
    lessons_path = Path('.').resolve() / 'lessons'
    return {
        'title': 'Kanonické lekce',
        'description': 'Seznam udržovaných lekcí bez ladu a skladu.',
        'long_description': textwrap.dedent("""
            Seznam udržovaných lekcí bez ladu a skladu.

            Jednotlivé kurzy jsou poskládané z těchto materiálů
            (a doplněné jinými).
        """),
        'sessions': [
            {
                'title': f'`{category_path.name}`',
                'slug': category_path.name,
                'materials': [
                    {'lesson': f'{category_path.name}/{lesson_path.name}'}
                    for lesson_path in sorted(category_path.iterdir())
                    if lesson_path.is_dir()
                ]
            }
            for category_path in sorted(lessons_path.iterdir())
        ]
    }
