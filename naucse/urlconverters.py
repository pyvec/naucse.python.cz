import re

from werkzeug.routing import BaseConverter


_converters = {}


def _converter(name):
    def decorator(cls):
        _converters[name] = cls
        return cls
    return decorator


def register_url_converters(app):
    for name, cls in _converters.items():
        app.url_map.converters[name] = cls

@_converter('course')
class CourseConverter(BaseConverter):
    regex = r'(([0-9]{4}|course)/[^/]+)|lessons'

    # XXX: The URLs should really be "courses/<...>",
    # but we don't have good redirects yet,, so leave them at
    # "course/<...>"

    def to_python(self, value):
        if value.startswith('course/'):
            value = value.replace('course/', 'courses/')
        return value

    def to_url(self, value):
        if value.startswith('courses/'):
            return value.replace('courses/', 'course/', 1)
        return value


@_converter('lesson')
class LessonConverter(BaseConverter):
    regex = r'[^/]+/[^/]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


@_converter('is_input')
class IsInputConverter(BaseConverter):
    regex = r'in|out'

    def to_python(self, value):
        return (value == 'in')

    def to_url(self, is_input):
        if is_input:
            return 'in'
        else:
            return 'out'
