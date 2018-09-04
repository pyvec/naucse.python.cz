import datetime
from functools import singledispatch
import textwrap

import attr
import dateutil.tz

import naucse_render

# XXX: Different timezones?
_TIMEZONE = 'Europe/Prague'


def load_dict(cls, data):
    kwargs = {}
    for attribute in attr.fields(cls):
        construct = attribute.metadata.get('naucse.construct')
        if construct:
            kwargs[attribute.name] = construct(kwargs, data)
        elif attribute.name not in data and attribute.default is not attr.NOTHING:
            kwargs[attribute.name] = attribute.default
        elif attribute.name not in data and attribute.metadata.get('naucse.default', attr.NOTHING) is not attr.NOTHING:
            kwargs[attribute.name] = attribute.metadata['naucse.default']
        else:
            item = data[attribute.name]
            loader = attribute.metadata.get('naucse.load', lambda i: i)
            kwargs[attribute.name] = loader(item)
    return cls(**kwargs)


def load_list(cls, data, index_key=None):
    if index_key:
        return [load_dict(cls, {**item, index_key: i}) for i, item in enumerate(data)]
    else:
        return [load_dict(cls, item) for item in data]


def field(default=attr.NOTHING, construct=None, doc=None):
    schema = {}
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        metadata={
            'naucse.default': default,
            'naucse.construct': construct,
            'naucse.schema': schema,
        }
    )


def string_field(default=attr.NOTHING, construct=None, doc=None):
    schema = {'type': 'string'}
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        metadata={
            'naucse.default': default,
            'naucse.construct': construct,
            'naucse.loader': str,
            'naucse.schema': schema,
        }
    )


def int_field(default=attr.NOTHING, doc=None):
    schema = {'type': 'integer'}
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        default=default,
        converter=int,
        metadata={
            'naucse.schema': schema,
        }
    )


def date_field(default=attr.NOTHING, construct=None, optional=False, doc=None):
    schema = {'type': 'string', 'format': 'date'}
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        metadata={
            'naucse.schema': schema,
            'naucse.default': default,
            'naucse.construct': construct,
            'naucse.load': lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
        }
    )


def datetime_field(default=attr.NOTHING, construct=None, optional=False, doc=None):
    schema = {'type': 'string', 'format': 'date'}
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        metadata={
            'naucse.schema': schema,
            'naucse.default': default,
            'naucse.construct': construct,
            'naucse.load': time_from_string,
        }
    )


def object_field(item_type=object, doc=None):
    schema = {
        'type': 'object',
        'properties': {'$ref': '#/definitions/{item_type.__name__}'},
    }
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        metadata={
            'naucse.loader': item_type,
            'naucse.schema': schema,
        }
    )


def dict_field(item_type=object, factory=None, doc=None):
    schema = {
        'type': 'object',
        'properties': {'$ref': '#/definitions/{item_type.__name__}'},
    }
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        factory=factory,
        metadata={
            'naucse.default': {},
            'naucse.schema': schema,
        }
    )


def list_field(item_type, doc=None):
    schema = {
        'type': 'array',
        'items': {'$ref': '#/definitions/{item_type.__name__}'},
    }
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        metadata={
            'naucse.schema': schema,
            'naucse.load': lambda data: load_list(item_type, data),
        }
    )


# XXX: index
def list_dict_field(item_type, key, doc=None, index_key=None):
    schema = {
        'type': 'array',
        'items': {'$ref': '#/definitions/{item_type.__name__}'},
    }
    if doc:
        schema['description'] = textwrap.dedent(doc)
    return attr.ib(
        metadata={
            'naucse.schema': schema,
            'naucse.dumper': lambda data, **k: to_dict(list(data.values())),
            'naucse.load': lambda data: {
                key(i): i
                for i in load_list(item_type, data, index_key=index_key)},
        }
    )


def model(init=True):
    def _model_decorator(cls):
        cls = attr.s(init=init)(cls)
        return cls
    return _model_decorator


@singledispatch
def to_dict(obj, urls=None):
    if urls and type(obj) in urls:
        return {'$ref': urls[type(obj)](obj)}
    result = {}
    for attribute in attr.fields(type(obj)):
        dumper = attribute.metadata.get('naucse.dumper', to_dict)
        result[attribute.name] = dumper(getattr(obj, attribute.name), urls=urls)
    return result


@to_dict.register(dict)
def _(obj, **kwargs):
    return {str(k): to_dict(v, **kwargs) for k, v in obj.items()}


@to_dict.register(list)
def _(obj, **kwargs):
    return [to_dict(v, **kwargs) for v in obj]


@to_dict.register(str)
@to_dict.register(int)
@to_dict.register(type(None))
def _(obj, **kwargs):
    return obj


@to_dict.register(datetime.date)
def _(obj, **kwargs):
    return obj.strftime('%Y-%m-%d')


@to_dict.register(datetime.time)
def _(obj, **kwargs):
    return obj.strftime('%H:%M')


def time_from_string(time_string):
    # XXX: Seconds?
    hour, minute = time_string.split(':')
    hour = int(hour)
    minute = int(minute)
    tzinfo = dateutil.tz.gettz(_TIMEZONE)
    return datetime.time(hour, minute, tzinfo=tzinfo)


@model()
class Material:
    title = string_field(doc='Human-readable title')
    slug = string_field(default=None, doc='Machine-friendly identifier')
    type = string_field(default='page')
    url = string_field(default=None)


@model()
class Session:
    title = string_field(doc='Human-readable title')
    slug = string_field(doc='Machine-friendly identifier')
    index = int_field(doc='Number of the session')
    date = date_field(default=None,
                      doc='''
                        Date when this session is taught.
                        Missing for self-study materials.''')
    materials = list_field(Material)
    start_time = datetime_field(
        default=None,
        doc='Times of day when the session starts.')
    start_time = datetime_field(
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


@model()
class Course:
    title = string_field(doc='Human-readable title')
    slug = string_field(doc='Machine-friendly identifier')
    subtitle = string_field(default=None, doc='Human-readable title')
    # XXX: index?
    sessions = list_dict_field(Session, key=lambda s: s.slug, index_key='index')
    vars = dict_field()
    start_date = date_field(
        construct=lambda kw, data: _min_or_none(s.date for s in kw['sessions'].values()),
        doc='Date when this starts, or None')
    end_date = date_field(
        construct=lambda kw, data: _max_or_none(s.date for s in kw['sessions'].values()),
        doc='Date when this starts, or None')
    place = string_field(
        default=None,
        doc='Textual description of where the course takes place')
    time = string_field(
        default=None,
        doc='Textual description of the time of day the course takes place')
    description = string_field(
        default=None,
        doc='Short description of the course (about one line).')
    long_description = string_field(
        default=None,
        doc='Long description of the course (up to several paragraphs)')
    default_time = field(
        default=None,
        construct=lambda kw, data: {
            k: time_from_string(data['default_time'][k])
            for k in ('start', 'end')} if 'default_time' in data else None,
        doc='Times of day when sessions notmally take place. May be null.')

    @classmethod
    def load_local(cls, root, slug):
        data = naucse_render.get_course(slug, version=1)
        return load_dict(cls, {**data, 'slug': slug})

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


@model()
class RunYear:
    year = int_field()
    runs = dict_field(Course, factory=dict)

    def __iter__(self):
        # XXX: Sort by ... start date?
        return iter(self.runs.values())


@model(init=False)
class Root:
    courses = dict_field(Course)
    run_years = dict_field(RunYear)

    def __init__(self, path):
        self.path = path

        self.courses = {}
        for course_path in (path / 'courses').iterdir():
            if (course_path / 'info.yml').is_file():
                slug = 'courses/' + course_path.name
                course = Course.load_local(self, slug)
                self.courses[slug] = course

        self.run_years = {}
        for year_path in sorted((path / 'runs').iterdir()):
            if year_path.is_dir():
                year = int(year_path.name)
                self.run_years[int(year_path.name)] = run_year = RunYear(year=year)
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
