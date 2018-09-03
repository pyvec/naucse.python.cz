from functools import partial

from flask import abort
from werkzeug.routing import BaseConverter

from naucse.models import Lesson


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


@_converter('course')
class CourseConverter(ModelConverter):
    regex = r'([0-9]{4}|course)/[^/]+'

    def to_python(self, value):
        year, slug = value.split('/')
        if year in ('course', 'courses'):
            return self.model.courses['courses/' + slug]
        else:
            runs = self.model.runs
            try:
                return runs[int(year), slug]
            except KeyError:
                abort(404)

    def to_url(self, value):
        # the converter can be called with a dict mimicking a course
        if isinstance(value, dict):
            value = value["slug"]

        if isinstance(value, str):
            if "/" not in value:  # XXX
                value = "course/" + value
            value = self.to_python(value)

        if value.slug.startswith('courses/'):
            return value.slug.replace('courses/', 'course/', 1)
        return value.slug


@_converter('lesson_slug')
class LessonSlugConverter(ModelConverter):
    regex = r'[^/]+/[^/]+'

    def to_url(self, value):
        if isinstance(value, Lesson):
            return value.slug

        # the converter can be called with a dict mimicking a lesson
        elif isinstance(value, dict):
            return value["slug"]

        return value


@_converter('lesson')
class LessonConverter(LessonSlugConverter):

    def to_python(self, value):
        try:
            return self.model.get_lesson(value)
        except LookupError:
            abort(404)

    def to_url(self, value):
        # the converter can be called with a dict mimicking a lesson
        if isinstance(value, dict):
            return value["slug"]

        if isinstance(value, str):
            value = self.to_python(value)
        return value.slug


def register_url_converters(app, model):
    for name, cls in _converters.items():
        app.url_map.converters[name] = partial(cls, model)
