"""
Retreive course meta-information

Reads source YAML files and merges them to one JSON, with
render info for items.
"""

from pathlib import Path
import datetime
import textwrap

from .load import read_yaml
from .markdown import convert_markdown


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


def get_course(course_slug: str, *, path='.', version=None):
    """Get information about the course as a JSON-compatible dict
    """
    # naucse's YAML files grew organically and use confusing terminology.
    # Many fields are renamed for the API; this function does the renaming
    # from (possibly old-style) YAML.

    base_path = Path(path).resolve()

    # Find location on disk based on the course slug
    if course_slug == 'lessons':
        # special course containing all lessons
        info = get_canonical_lessons_info(path)
        path_parts = None
    else:
        parts = course_slug.split('/')
        if len(parts) == 1 or (len(parts) == 2 and parts[0] == 'courses'):
            # 'courses/FOO': a self-study course, in directory courses/FOO
            path_parts = 'courses', parts[-1]
        elif len(parts) == 2:
            # 'YEAR/BAR': a "run" in runs/YEAR/BAR
            path_parts = 'runs', *parts
        else:
            raise ValueError(f'Invalid course slug')

        info = read_yaml(
            base_path, *path_parts, 'info.yml',
            source_key='source_file',
        )

    # We are only concerned about the content; naucse itself will determine
    # what courses it deems canonical/meta.
    info.pop('meta', None)
    info.pop('canonical', None)

    # See if this course is derived from another course
    # (which means session data in this course's YAML hold only updates
    # to the base_course)
    base_slug = info.get('derives', None)
    if base_slug:
        base_course = read_yaml(base_path, 'courses', base_slug, 'info.yml')
    else:
        base_course = {}

    # Rename "plan" to "sessions"
    for d in info, base_course:
        if 'plan' in d:
            d['sessions'] = d.pop('plan')

    # Convert Markdown in "long_description" to HTML
    if 'long_description' in info:
        info['long_description'] = convert_markdown(info['long_description'])

    # Rename the text field "time" to "time_description"
    if 'time' in info:
        info['time_description'] = info.pop('time')

    for session in info['sessions']:
        session['source_file'] = info['source_file']

        # Handle session "inheritance" in derived courses
        base = session.pop('base', None)
        if base:
            for base_session in base_course['sessions']:
                if base_session['slug'] == base:
                    break
            else:
                raise ValueError(f'Session {session} not found in base course')
            session.update(merge_dict(base_session, session))

        # Update all materials
        for material in session.get('materials', []):
            update_material(material, vars=info.get('vars'), path=base_path)

        # Convert Markdown in "description" to HTML
        if 'description' in session:
            session['description'] = convert_markdown(session['description'])

        if path_parts:
            # Get coverpage content
            page_path = base_path.joinpath(
                *path_parts, 'sessions', session['slug']
            )
            if page_path.exists():
                session['pages'] = {}
                for page_md_path in page_path.glob('*.md'):
                    session['pages'][page_md_path.stem] = {
                        'content': convert_markdown(page_md_path.read_text()),
                    }

    result = encode_dates(info)
    return {
        'api_version': [0, 0],  # Version "0.0"
        'course': result,
    }


def update_material(material, vars=None, *, path):
    """Update material entry: mainly, add computed fields"""
    # All materials should have a "type", as used for the icon in lists
    lesson_slug = material.pop('lesson', None)
    if lesson_slug:
        # Link to a lesson on naucse
        material['lesson_slug'] = lesson_slug
        if material.pop('url', None):
            pass
            # XXX: raise ValueError(f'Material {material} has URL')
        material.setdefault('type', 'lesson')
        if 'title' not in material:
            # Set title based on the referenced lesson
            lesson_info = read_yaml(path, 'lessons', lesson_slug, 'info.yml')
            material['title'] = lesson_info['title']
    else:
        # External link (or link-less entry)
        url = material.pop('url', None)
        if url:
            material['external_url'] = url
            # XXX: Probably a bug; this should be just 'link'
            material.setdefault('type', 'none-link')
        else:
            material.setdefault('type', 'special')


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


def get_canonical_lessons_info(path):
    """Return data on the special course that lists all lessons"""

    # XXX: This is not useful in "forks"
    lessons_path = path.resolve() / 'lessons'
    return {
        'title': 'Kanonické lekce',
        'description': 'Seznam udržovaných lekcí bez ladu a skladu.',
        'long_description': convert_markdown(textwrap.dedent("""
            Seznam udržovaných lekcí bez ladu a skladu.

            Jednotlivé kurzy jsou poskládané z těchto materiálů
            (a doplněné jinými).
        """)),
        'source_file': 'lessons',
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
            if category_path.is_dir()
        ]
    }
