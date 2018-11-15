import datetime
from functools import singledispatch
import textwrap
import importlib

import dateutil.tz
import jsonschema

from naucse.edit_info import get_local_edit_info
from naucse.htmlparser import sanitize_html
import naucse_render

# XXX: Different timezones?
_TIMEZONE = 'Europe/Prague'


class NoURL(LookupError):
    """An object's URL could not be found"""

class NoURLType(NoURL):
    """The requested URL type is not available"""


class _Nothing:
    """Missing value"""
    def __bool__(self):
        return False

NOTHING = _Nothing()


models = {}


def get_schema(cls, *, is_input):
    definitions = {
        c.__name__: c.get_schema(is_input=is_input) for c in models.values()
    }
    definitions.update({
        'ref': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                '$ref': {
                    'type': 'string',
                    'format': 'uri',
                },
            },
        },
        'api_version': {
            'type': 'array',
            'items': {'type': 'integer'},
            'minItems': 2,
            'maxItems': 2,
            'description': textwrap.dedent("""
                Version of the information, and of the schema,
                as two integers – [major, minor].
                The minor version is increased on every change to the
                schema that keeps backwards compatibility for forks
                (i.e. input data).
                The major version is increased on incompatible changes.
            """),
        },
    })
    return {
        '$ref': f'#/definitions/{cls.__name__}',
        '$schema': 'http://json-schema.org/draft-06/schema#',
        'definitions': definitions,
    }


def schema_object(cls, *, allow_ref=True):
    schema_object = {
        '$ref': f'#/definitions/{cls.__name__}',
    }
    if allow_ref:
        return {
            'anyOf': [
                schema_object,
                {
                    '$ref': f'#/definitions/ref',
                }
            ],
        }
    else:
        return schema_object



class Model:
    def __init__(self, *, parent):
        self.root = parent.root
        self._parent = parent

    @classmethod
    def load(cls, data, **kwargs):
        instance = cls(**kwargs)
        for name, field in cls._naucse__fields.items():
            field.load(instance, data)
        return instance

    def dump(self, expanded=True):
        result = {}
        try:
            result['api_url'] = api_url = self.get_url('api', external=True)
        except NoURL:
            pass
        else:
            if not expanded:
                return {'$ref': api_url}

        try:
            result['url'] = self.get_url(external=True)
        except NoURL:
            pass
        for name, field in self._naucse__fields.items():
            field.dump(self, result)
        jsonschema.validate(result, get_schema(type(self), is_input=False))  # XXX
        if expanded:
            jsonschema.validate(result, get_schema(type(self), is_input=False))
            result['$schema'] = self.root._schema_url_for(
                    type(self), external=True, is_input=False)
        return result

    @classmethod
    def get_schema(cls, *, is_input):
        result = {
            'type': 'object',
            'title': cls.__name__,
            'additionalProperties': False,
            'required': [
                name for name, field in cls._naucse__fields.items()
                if field.required_in_schema(is_input=is_input)
            ],
            'properties': {
                'url': {
                    'type': 'string',
                    'format': 'uri',
                },
                'api_url': {
                    'type': 'string',
                    'format': 'uri',
                },
                'api_version': {'$ref': '#/definitions/api_version'},
            },
        }
        if cls.__doc__:
            retult['description'] == cls.__doc__
        for name, field in cls._naucse__fields.items():
            result['properties'][field.name] = field.get_schema(is_input=is_input)
        return result

    def __init_subclass__(cls):
        models[cls.__name__] = cls
        cls._naucse__fields = {}
        for attr_name, attr_value in list(vars(cls).items()):
            if isinstance(attr_value, Field):
                delattr(cls, attr_name)
                cls._naucse__fields[attr_name] = attr_value
        return cls

    def get_url(self, url_type='web', *, external=False):
        return self.root._url_for(self, url_type=url_type, external=external)


class Field:
    def __init__(
        self, *,
        optional=False, default=NOTHING, factory=None, doc=None,
        convert=None, construct=None, data_key=None, choices=None,
        input_optional=False,  # XXX
    ):
        if doc:
            self.doc = doc
        else:
            self.doc = self.__doc__
        self.optional = optional
        self.default = default
        self.factory = factory
        if convert:
            self.convert = convert
        if construct:
            self.construct = construct
        if data_key:
            self.data_key = data_key
        self.choices = choices
        self.input_optional = input_optional

    def __set_name__(self, instance, name):
        self.name = name
        if not hasattr(self, 'data_key'):
            self.data_key = name

    def load(self, instance, data):
        value = self.construct(instance, data)
        if value is not NOTHING:
            setattr(instance, self.name, value)

    def construct(self, instance, data):
        try:
            value = data[self.data_key]
        except KeyError:
            if self.optional:
                return NOTHING
            if self.factory:
                return self.factory()
            if self.default is not NOTHING:
                return self.default
            raise
        else:
            return self.convert(instance, data, value)
        return value

    def convert(self, instance, data, value):
        return value

    def dump(self, instance, data):
        # XXX: Bad name
        try:
            value = getattr(instance, self.name)
        except AttributeError:
            return
        data[self.data_key] = self.unconvert(value)

    def unconvert(self, value):
        return to_jsondata(value)

    def get_schema(self, *, is_input):
        schema = {}
        if self.choices is not None:
            schema['enum'] = list(self.choices)
        return schema

    def required_in_schema(self, *, is_input):
        if self.optional:
            return False
        if is_input and self.default is not NOTHING:
            return False
        if is_input and self.factory is not None:
            return False
        if is_input and self.input_optional:
            return False
        return True


def field(**kwargs):
    def _field_decorator(cls):
        return cls(**kwargs)
    return _field_decorator


class StringField(Field):
    def get_schema(self, *, is_input):
        return {**super().get_schema(is_input=is_input), 'type': 'string'}


class IntField(Field):
    def get_schema(self, *, is_input):
        return {**super().get_schema(is_input=is_input), 'type': 'integer'}


class DateField(Field):
    def get_schema(self, *, is_input):
        return {
            **super().get_schema(is_input=is_input),
            'type': 'string',
            'format': 'date',
        }

    def convert(self, instance, data, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()


class DateTimeField(Field):
    def get_schema(self, *, is_input):
        return {**super().get_schema(is_input=is_input), 'type': 'string',}


class DictField(Field):
    def __init__(self, item_type, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type

    def convert(self, instance, data, value):
        return {k: self.item_type.load(v, parent=instance)
                for k, v in value.items()}

    def get_schema(self, *, is_input):
        return {
            **super().get_schema(is_input=is_input),
            'type': 'object',
            'additionalProperties': schema_object(self.item_type, allow_ref=not is_input)
        }


class ListField(Field):
    def __init__(self, item_type, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type

    def get_schema(self, *, is_input):
        return {
            **super().get_schema(is_input=is_input),
            'type': 'array',
            'items': schema_object(self.item_type, allow_ref=not is_input),
        }

    def convert(self, instance, data, value):
        return [self.item_type.load(d, parent=instance) for d in value]


class StringListField(Field):
    def get_schema(self, *, is_input):
        return {
            **super().get_schema(is_input=is_input),
            'type': 'array',
            'items': {
                'type': 'string',
            },
        }


class ListDictField(Field):
    def __init__(self, item_type, *, key_attr, index_key, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type
        self.key_attr = key_attr
        self.index_key = index_key

    def get_schema(self, *, is_input):
        return {
            **super().get_schema(is_input=is_input),
            'type': 'array',
            'items': schema_object(self.item_type, allow_ref=not is_input),
        }

    def convert(self, instance, data, value):
        result = {}
        for idx, item_data in enumerate(value):
            item_data[self.index_key] = idx
            item = self.item_type.load(item_data, parent=instance)
            result[getattr(item, self.key_attr)] = item
        return result

    def unconvert(self, value):
        return [to_jsondata(v) for v in value.values()]


class UrlField(Field):
    def get_schema(self, *, is_input):
        return {
            **super().get_schema(is_input=is_input),
            'type': 'string',
            'format': 'url',
        }

class ObjectField(Field):
    def __init__(self, item_type, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type

    def convert(self, instance, data, value):
        return self.item_type.load(value, parent=instance)

    def get_schema(self, *, is_input):
        return schema_object(self.item_type, allow_ref=not is_input)


@property
def parent_property(self):
    return self._parent


def model(init=True):
    def _model_decorator(cls):
        cls = attr.s(init=init)(cls)
        return cls
    return _model_decorator


@singledispatch
def to_jsondata(obj, urls=None):
    raise TypeError(type(obj))


@to_jsondata.register(Model)
def _(obj, **kwargs):
    try:
        url = obj.get_url(url_type='api', external=True)
    except NoURL:
        return obj.dump(expanded=False, **kwargs)
    else:
        return {'$ref': url}


@to_jsondata.register(dict)
def _(obj, **kwargs):
    return {str(k): to_jsondata(v, **kwargs) for k, v in obj.items()}


@to_jsondata.register(list)
def _(obj, **kwargs):
    return [to_jsondata(v, **kwargs) for v in obj]


@to_jsondata.register(str)
@to_jsondata.register(int)
@to_jsondata.register(type(None))
def _(obj, **kwargs):
    return obj


@to_jsondata.register(datetime.date)
def _(obj, **kwargs):
    return obj.strftime('%Y-%m-%d')


@to_jsondata.register(datetime.time)
def _(obj, **kwargs):
    return obj.strftime('%H:%M')


def time_from_string(time_string):
    # XXX: Seconds?
    hour, minute = time_string.split(':')
    hour = int(hour)
    minute = int(minute)
    tzinfo = dateutil.tz.gettz(_TIMEZONE)
    return datetime.time(hour, minute, tzinfo=tzinfo)


class RenderCall(Model):
    entrypoint = StringField(doc="Arca entrypoint")
    args = Field(default=(), doc="Arguments for the Arca call")
    kwargs = Field(factory=dict, doc="Arguments for the Arca call")

    def call(self):
        module, func_name = self.entrypoint.split(':')
        func = getattr(importlib.import_module(module), func_name)
        return func(*self.args, **self.kwargs)


class Page(Model):
    title = StringField(doc='Human-readable title')
    slug = StringField(doc='Machine-friendly identifier')

    # XXX: License object?
    license = StringField(
        choices=("cc-by-sa-40", "cc0"),
        doc=textwrap.dedent('''
            Identifier of the licence under which content is available.
            Note that Naucse supports only a limited set of licences.''')
    )

    attribution = StringListField(doc='Authorship information')

    license_code = StringField(
        optional=True,
        choices=("cc-by-sa-40", "cc0"),
        doc=textwrap.dedent('''
            Identifier of the licence under which code is available.
            Note that Naucse supports only a limited set of licences.''')
    )

    render_call = ObjectField(RenderCall)

    material = parent_property

    @property
    def session(self):
        return self.material.session

    @property
    def course(self):
        return self.material.session.course

    def get_content(self):
        result = self.render_call.call()

        def lesson_url(lesson, page='index', **kw):
            lesson = self.course.get_material(lesson)
            page = lesson.pages[page]
            return page.get_url(**kw)

        return sanitize_html(
            result,
            url_for={
                'lesson': lesson_url,
            }
        )


class Material(Model):
    title = StringField(doc='Human-readable title')
    slug = StringField(
        optional=True, doc='Machine-friendly identifier')
    type = StringField(default='page')
    external_url = UrlField(optional=True)
    pages = DictField(Page, optional=True)

    session = parent_property

    def get_url(self, url_type='web', **kwargs):
        if url_type != 'web':
            raise NoURLType(url_type)
        try:
            return self.external_url
        except AttributeError:
            try:
                pages = self.pages
            except AttributeError:
                return None
            return pages['index'].get_url(**kwargs)

    @property
    def course(self):
        return self.session.course


def _construct_time(which):
    def _construct(session, data):
        try:
            value = data[f'{which}_time']
        except KeyError:
            time = getattr(session.course, f'default_{which}_time')
            if time is None:
                return NOTHING
        else:
            try:
                return datetime.datetime.strftime('%Y-%m-%d %H:%M:%S', value)
            except ValueError:
                pass
            time = datetime.datetime.strftime('%H:%M:%s', value)
        date = session.date
        if date is None:
            return NOTHING
        return datetime.datetime.combine(date, time)
    return _construct


class Session(Model):
    title = StringField(doc='Human-readable title')
    slug = StringField(doc='Machine-friendly identifier')
    index = IntField(default=None, doc='Number of the session')
    date = DateField(optional=True,
                      doc='''
                        Date when this session is taught.
                        Missing for self-study materials.''')
    materials = ListField(Material)
    start_time = DateTimeField(
        optional=True,
        construct=_construct_time('start'),
        doc='Times of day when the session starts.')
    end_time = DateTimeField(
        optional=True,
        construct=_construct_time('end'),
        doc='Times of day when the session ends.')

    course = parent_property

    @property  # XXX: Reify? Load but not export?
    def _materials_by_slug(self):
        return {mat.slug: mat for mat in self.materials if mat.slug}

    def get_material(self, slug):
        print(slug)
        return self._materials_by_slug[slug]


def _max_or_none(sequence):
    return max([m for m in sequence if m is not None], default=NOTHING)

def _min_or_none(sequence):
    return min([m for m in sequence if m is not None], default=NOTHING)


class Course(Model):
    title = StringField(doc='Human-readable title')
    slug = StringField(optional=True, doc='Machine-friendly identifier')
    subtitle = StringField(optional=True, doc='Human-readable title')
    sessions = ListDictField(Session, key_attr='slug', index_key='index')
    vars = Field(factory=dict)
    start_date = DateField(
        construct=lambda instance, data: _min_or_none(getattr(s, 'date', None) for s in instance.sessions.values()),
        optional=True,
        doc='Date when this starts, or None')
    end_date = DateField(
        construct=lambda instance, data: _max_or_none(getattr(s, 'date', None) for s in instance.sessions.values()),
        optional=True,
        doc='Date when this starts, or None')
    place = StringField(
        optional=True,
        doc='Textual description of where the course takes place')
    time = StringField(
        optional=True,
        doc='Textual description of the time of day the course takes place')
    description = StringField(
        optional=True,
        doc='Short description of the course (about one line).')
    long_description = StringField(
        optional=True,
        doc='Long description of the course (up to several paragraphs)')
    vars = Field(
        default={},
        doc='Variables for rendering a page of content.')

    # XXX: is this subclassing necessary?
    @field(optional=True)
    class default_time(Field):
        '''Times of day when sessions notmally take place. May be null.'''
        def convert(self, instance, data, value):
            return {
                'start': time_from_string(data['default_time']['start']),
                'end': time_from_string(data['default_time']['end']),
            }

    @classmethod
    def load_local(cls, parent, slug):
        data = naucse_render.get_course(slug, version=1)
        jsonschema.validate(data, get_schema(cls, is_input=True))
        result = cls.load(data, parent=parent)
        result.slug = slug
        return result

    @property
    def default_start_time(self):
        if getattr(self, 'default_time', None) is None:  # XXX
            return None
        return self.default_time['start']

    @property
    def default_end_time(self):
        if getattr(self, 'default_time', None) is None:  # XXX
            return None
        return self.default_time['end']

    def get_material(self, slug):
        # XXX: Check duplicates
        for session in self.sessions.values():
            for material in session.materials:
                try:
                    mat_slug = material.slug
                except AttributeError:
                    continue
                if mat_slug == slug:
                    return material
        raise LookupError(slug)


class RunYear(Model):
    year = IntField()
    runs = DictField(Course, factory=dict)

    def __init__(self, year, parent):
        super().__init__(parent=parent)
        self.year = year
        self.runs = {}

    def __iter__(self):
        # XXX: Sort by ... start date?
        return iter(self.runs.values())


class Root(Model):
    courses = DictField(Course)
    run_years = DictField(RunYear)

    def __init__(self, *, url_factories, schema_url_factory):
        self.root = self
        self.url_factories = url_factories
        self.schema_url_factory = schema_url_factory

        self.courses = {}
        self.run_years = {}

    def load_local(self, path):
        for course_path in (path / 'courses').iterdir():
            if (course_path / 'info.yml').is_file():
                slug = 'courses/' + course_path.name
                course = Course.load_local(self, slug)
                assert course, course
                self.courses[slug] = course

        for year_path in sorted((path / 'runs').iterdir()):
            if year_path.is_dir():
                year = int(year_path.name)
                run_year = RunYear(year=year, parent=self)
                run_year.edit_info = get_local_edit_info(year_path)
                self.run_years[int(year_path.name)] = run_year
                for course_path in year_path.iterdir():
                    if (course_path / 'info.yml').is_file():
                        slug = f'{year_path.name}/{course_path.name}'
                        course = Course.load_local(self, slug)
                        run_year.runs[slug] = course

        self.courses['lessons'] = Course.load_local(self, 'lessons')

        self.edit_info = get_local_edit_info(path)
        self.runs_edit_info = get_local_edit_info(path / 'runs')

    def get_course(self, slug):
        if slug == 'lessons':
            return self.courses[slug]
        year, identifier = slug.split('/')
        if year == 'courses':
            return self.courses[slug]
        else:
            return self.run_years[int(year)].runs[slug]

    def runs_from_year(self, year):
        try:
            runs = self.run_years[year].runs
        except KeyError:
            return []
        return list(runs.values())

    def _schema_url_for(self, cls, is_input, external=False):
        return self.schema_url_factory(
            cls, _external=external, is_input=is_input)

    def _url_for(self, obj, url_type='web', *, external=False):
        try:
            urls = self.url_factories[url_type]
        except KeyError:
            raise NoURLType(url_type)
        try:
            url_for = urls[type(obj)]
        except KeyError:
            raise NoURL(type(obj))
        return url_for(obj, _external=external)
