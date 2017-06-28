from functools import partial

from flask import abort
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


@_converter('course')
class CourseConverter(ModelConverter):
    regex = r'([0-9]{4}|course)/[^/]+'

    def to_python(self, value):
        year, slug = value.split('/')
        if year == "course":
            return self.model.courses[slug]
        else:
            try:
                return self.model.runs[int(year), slug]
            except KeyError:
                abort(404)

    def to_url(self, value):
        if isinstance(value, str):
            if "/" not in value: # XXX
                value = "course/"+value
            value = self.to_python(value)
        return value.slug


@_converter('lesson')
class LessonConverter(ModelConverter):
    regex = r'[^/]+/[^/]+'

    def to_python(self, value):
        try:
            return self.model.get_lesson(value)
        except LookupError:
            abort(404)

    def to_url(self, value):
        if isinstance(value, str):
            value = self.to_python(value)
        return value.slug


def register_url_converters(app, model):
    for name, cls in _converters.items():
        app.url_map.converters[name] = partial(cls, model)
