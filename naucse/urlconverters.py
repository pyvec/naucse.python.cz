import re

from functools import partial

from werkzeug.routing import BaseConverter


class ModelConverter(BaseConverter):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model


_converters = {}


def _converter(name):
    def decorator(cls):
        _converters[name] = cls
        return cls
    return decorator


def register_url_converters(app, model):
    for name, cls in _converters.items():
        app.url_map.converters[name] = partial(cls, model)


def slug_to_course(model, slug):
    if slug.startswith('course/'):
        slug = slug.replace('course/', 'courses/')
    return model.get_course(slug)

def course_to_slug(model, course):
    if isinstance(course, str):
        return model.get_course(course)

    # XXX: The URLs should really be "courses/<...>",
    # but we don't have good redirects yet,, so leave them at
    # "course/<...>"
    if course.slug.startswith('courses/'):
        return course.slug.replace('courses/', 'course/', 1)

    return course.slug

@_converter('course')
class CourseConverter(ModelConverter):
    regex = r'([0-9]{4}|course)/[^/]+'

    def to_python(self, value):
        return slug_to_course(self.model, value)

    def to_url(self, course):
        return course_to_slug(self.model, course)


@_converter('material')
class MaterialConverter(ModelConverter):
    regex = CourseConverter.regex + r'/([^/]+/[^/]+)'

    def to_python(self, value):
        regex = r'(?P<course>[^/]+/[^/]+)/(?P<lesson>[^/]+/[^/]+)'
        match = re.match(regex, value)
        course = slug_to_course(self.model, match.group('course'))
        return course.get_material(match.group('lesson'))

    def to_url(self, material):
        course_url = course_to_slug(self.model, material.course)
        return f'{course_url}/{material.slug}'


@_converter('is_input')
class IsInputConverter(ModelConverter):
    regex = r'in|out'

    def to_python(self, value):
        return (value == 'in')

    def to_url(self, is_input):
        if is_input:
            return 'in'
        else:
            return 'out'
