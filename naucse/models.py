import datetime
from functools import singledispatch
import textwrap

#import attr
from attr import NOTHING
import dateutil.tz

import naucse_render

# XXX: Different timezones?
_TIMEZONE = 'Europe/Prague'


class NoURL(LookupError):
    """An object's URL could not be found"""


models = {}


def get_schema(cls):
    definitions = {c.__name__: c.get_schema() for c in models.values()}
    return {
        '$ref': f'#/definitions/{cls.__name__}',
        '$schema': 'http://json-schema.org/draft-06/schema#',
        'definitions': definitions,
    }



class Model:
    def __init__(self, *, root):
        self.root = root

    @classmethod
    def load(cls, data, **kwargs):
        instance = cls(**kwargs)
        for name, field in cls._naucse__fields.items():
            field.load(instance, data)
        return instance

    def dump(self, schema=False):  # XXX: context only?
        result = {}
        for name, field in self._naucse__fields.items():
            field.dump(self, result)
        if schema:
            result['$schema'] = self.root.schema_url_for(type(self))
        return result

    @classmethod
    def get_schema(cls):
        result = {
            'type': 'object',
            'title': cls.__name__,
            'description': cls.__doc__,
            'additionalProperties': False,
            'required': [
                name for name, field in cls._naucse__fields.items()
                if not field.optional
            ],
            'properties': {},
        }
        for name, field in cls._naucse__fields.items():
            result['properties'][field.name] = field.schema
        return result

    def __init_subclass__(cls):
        models[cls.__name__] = cls
        cls._naucse__fields = {}
        for attr_name, attr_value in list(vars(cls).items()):
            if isinstance(attr_value, Field):
                delattr(cls, attr_name)
                cls._naucse__fields[attr_name] = attr_value
        return cls


class Field:
    def __init__(
        self, *,
        optional=False, default=NOTHING, factory=None, doc=None,
        convert=None, construct=None,
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

    def __set_name__(self, instance, name):
        self.name = name

    @property
    def data_key(self):
        return self.name

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

    @property
    def schema(self):
        return {}


def field(**kwargs):
    def _field_decorator(cls):
        return cls(**kwargs)
    return _field_decorator


class StringField(Field):
    @property
    def schema(self):
        return {**super().schema, 'type': 'string'}


class IntField(Field):
    @property
    def schema(self):
        return {**super().schema, 'type': 'integer'}


class DateField(Field):
    @property
    def schema(self):
        return {
            **super().schema,
            'type': 'string',
            'format': 'date',
        }

    def convert(self, instance, data, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()


class DateTimeField(Field):
    @property
    def schema(self):
        return {**super().schema, 'type': 'string',}


class DictField(Field):
    def __init__(self, item_type, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type

    @property
    def schema(self):
        return {
            **super().schema,
            'type': 'object',
            'properties': {'$ref': f'#/definitions/{self.item_type.__name__}'},
        }


class ListField(Field):
    def __init__(self, item_type, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type

    @property
    def schema(self):
        return {
            **super().schema,
            'type': 'array',
            'items': {'$ref': f'#/definitions/{self.item_type.__name__}'},
        }

    def convert(self, instance, data, value):
        return [self.item_type.load(d, root=instance.root) for d in value]


class ListDictField(Field):
    def __init__(self, item_type, *, key_attr, index_key, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type
        self.key_attr = key_attr
        self.index_key = index_key

    @property
    def schema(self):
        return {
            **super().schema,
            'type': 'array',
            'items': {'$ref': f'#/definitions/{self.item_type.__name__}'},
        }

    def convert(self, instance, data, value):
        result = {}
        for idx, item_data in enumerate(value):
            item_data[self.index_key] = idx
            item = self.item_type.load(item_data, root=instance.root)
            result[getattr(item, self.key_attr)] = item
        return result

    def unconvert(self, value):
        return [to_jsondata(v) for v in value.values()]


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
        url = obj.root.api_url_for(obj)
    except NoURL:
        return obj.dump(**kwargs)
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


class Material(Model):
    title = StringField(doc='Human-readable title')
    slug = StringField(optional=True, doc='Machine-friendly identifier')
    type = StringField(default='page')
    url = StringField(optional=True)


class Session(Model):
    title = StringField(doc='Human-readable title')
    slug = StringField(doc='Machine-friendly identifier')
    index = IntField(doc='Number of the session')
    date = DateField(default=None,
                      doc='''
                        Date when this session is taught.
                        Missing for self-study materials.''')
    materials = ListField(Material)
    start_time = DateTimeField(
        default=None,
        doc='Times of day when the session starts.')
    start_time = DateTimeField(
        default=None,
        doc='Times of day when the session ends.')

    @property  # XXX: Reify? Load but not export?
    def _materials_by_slug(self):
        return {mat.slug: mat for mat in self.materials if mat.slug}

    def get_material(self, slug):
        return self._materials_by_slug[slug]


def _max_or_none(sequence):
    return max([m for m in sequence if m is not None], default=None)

def _min_or_none(sequence):
    return min([m for m in sequence if m is not None], default=None)


class Course(Model):
    title = StringField(doc='Human-readable title')
    slug = StringField(optional=True, doc='Machine-friendly identifier')
    subtitle = StringField(optional=True, doc='Human-readable title')
    # XXX: index?
    sessions = ListDictField(Session, key_attr='slug', index_key='index')
    vars = Field(factory=dict)
    start_date = DateField(
        construct=lambda instance, data: _min_or_none(s.date for s in instance.sessions.values()),
        doc='Date when this starts, or None')
    end_date = DateField(
        construct=lambda instance, data: _max_or_none(s.date for s in instance.sessions.values()),
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
    def load_local(cls, root, slug):
        data = naucse_render.get_course(slug, version=1)
        result = cls.load(data, root=root)
        result.slug = slug
        return result

    @property
    def default_start_time(self):
        if self.default_time is None:
            return None
        return self.default_time['start']

    @property
    def default_end_time(self):
        if self.default_time is None:
            return None
        return self.default_time['end']


class RunYear(Model):
    year = IntField()
    runs = DictField(Course, factory=dict)

    def __init__(self, year, root):
        self.root = root
        self.year = year
        self.runs = {}

    def __iter__(self):
        # XXX: Sort by ... start date?
        return iter(self.runs.values())


class Root(Model):
    courses = DictField(Course)
    run_years = DictField(RunYear)

    def __init__(self, path, urls):
        self.root = self
        self.path = path
        self.urls = urls

        self.courses = {}
        self.run_years = {}

        for course_path in (path / 'courses').iterdir():
            if (course_path / 'info.yml').is_file():
                slug = 'courses/' + course_path.name
                course = Course.load_local(self, slug)
                assert course, course
                self.courses[slug] = course

        for year_path in sorted((path / 'runs').iterdir()):
            if year_path.is_dir():
                year = int(year_path.name)
                self.run_years[int(year_path.name)] = run_year = RunYear(year=year, root=self)
                for course_path in year_path.iterdir():
                    if (course_path / 'info.yml').is_file():
                        slug = f'{year_path.name}/{course_path.name}'
                        course = Course.load_local(self, slug)
                        run_year.runs[slug] = course

    def get_course(self, slug):
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

    def api_url_for(self, obj):
        api_urls = self.urls['api']
        try:
            url_for = api_urls[type(obj)]
        except KeyError:
            raise NoURL(obj)
        return url_for(obj)

    def schema_url_for(self, model_type):
        return self.urls['schema'](model_type)
