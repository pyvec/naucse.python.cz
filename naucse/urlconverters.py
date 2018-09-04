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


@_converter('course')
class CourseConverter(ModelConverter):
    regex = r'([0-9]{4}|course)/[^/]+'

    def to_python(self, value):
        if value.startswith('course/'):
            value = value.replace('course/', 'courses/')
        return self.model.get_course(value)

    def to_url(self, course):
        # the converter can be called with a dict mimicking a course
        if isinstance(course, str):
            return self.model.get_course(course)

        # XXX: The URLs should really be "courses/<...>",
        # but we don't have good redirects yet,, so leave them at
        # "course/<...>"
        if course.slug.startswith('courses/'):
            return course.slug.replace('courses/', 'course/', 1)

        return course.slug
