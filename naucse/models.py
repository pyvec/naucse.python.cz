import datetime
from functools import singledispatch
import textwrap
import importlib
from pathlib import Path

import dateutil.tz
import jsonschema
import yaml

from naucse.edit_info import get_local_repo_info, get_repo_info
from naucse.sanitize import sanitize_html, sanitize_stylesheet
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


class reify:
    """Base class for a lazily computed property
    Subclasses should reimplement a `compute` method, which creates
    the value of the property. Then the value is stored and not computed again
    (unless deleted).
    """
    def __init__(self, func):
        self.func = func

    def __set_name__(self, cls, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        result = self.func(instance)
        setattr(instance, self.name, result)
        return result


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
        required = [
            name for name, field in cls._naucse__fields.items()
            if field.required_in_schema(is_input=is_input)
        ]
        if required:
            result['required'] = required
        if cls.__doc__:
            retult['description'] == cls.__doc__
        for name, field in cls._naucse__fields.items():
            if field.included_in_schema(is_input=is_input):
                field_schema = field.get_schema(is_input=is_input)
                result['properties'][field.name] = field_schema
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
        input_optional=False, output_only=False,  # XXX
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
        self.output_only = output_only

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

    def included_in_schema(self, *, is_input):
        if self.output_only and is_input:
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


def _set_prev_next(sequence, prev_next_attrs):
    if prev_next_attrs:
        sequence = list(sequence)
        prev_attr, next_attr = prev_next_attrs
        for prev, now, next in zip(
            [None] + sequence,
            sequence,
            sequence[1:] + [None],
        ):
            setattr(now, prev_attr, prev)
            setattr(now, next_attr, next)

class ListField(Field):
    def __init__(self, item_type, *, prev_next_attrs=None, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type
        self.prev_next_attrs = prev_next_attrs

    def get_schema(self, *, is_input):
        return {
            **super().get_schema(is_input=is_input),
            'type': 'array',
            'items': schema_object(self.item_type, allow_ref=not is_input),
        }

    def convert(self, instance, data, value):
        result = [self.item_type.load(d, parent=instance) for d in value]
        _set_prev_next(result, self.prev_next_attrs)
        return result


class MaterialListField(ListField):
    def convert(self, instance, data, value):
        result = super().convert(instance, data, value)
        seq = [mat for mat in result if getattr(mat, 'pages', None)]
        _set_prev_next(seq, ('prev', 'next'))
        return result


class StringListField(Field):
    def get_schema(self, *, is_input):
        return {
            **super().get_schema(is_input=is_input),
            'type': 'array',
            'items': {
                'type': 'string',
            },
        }


class HTMLListField(StringListField):
    def convert(self, instance, data, value):
        return [sanitize_html(d) for d in value]

    def get_schema(self, *, is_input):
        schema = super().get_schema(is_input=is_input)
        schema['items']['format'] = 'html-inline-fragment'
        return schema


class ListDictField(Field):
    def __init__(
        self, item_type, *, key_attr, index_key, prev_next_attrs=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.item_type = item_type
        self.key_attr = key_attr
        self.index_key = index_key
        self.prev_next_attrs = prev_next_attrs

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
        _set_prev_next(result.values(), self.prev_next_attrs)
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


class LicenseField(Field):
    def convert(self, instance, data, value):
        licenses = instance.root.licenses
        try:
            return licenses[value]
        except KeyError:
            keys = ', '.join(licenses)
            raise ValueError(
                f'{value} is not a valid licence (choose from {keys})'
            )

    def get_schema(self, *, is_input):
        # XXX: Get the actal licenses as options?
        if is_input:
            return {
                **super().get_schema(is_input=is_input),
                'type': 'string',
            }
        else:
            return schema_object(License)


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


class Solution(Model):
    def __init__(self, *, index=None, **kw):
        super().__init__(**kw)
        if index is not None:
            self.index = index

    index = IntField(default=None, doc='Number of the session')
    content = StringField(default='', doc='Solution content')

    page = parent_property

    @property
    def course(self):
        return self.page.course

    def get_content(self):
        return self.page.sanitize_content(self.content)


class StaticFile(Model):
    filename = StringField(doc='File name')
    path = StringField(doc='Full path to the file from the repository root')

    material = parent_property

    @property
    def course(self):
        return self.material.course

    def get_file_info(self):
        base, path = self.course.get_static_file_info(self.path)
        base = str(Path(base).resolve())
        return base, path


class Page(Model):
    # XXX: A page should not be allowed to be named "static"
    title = StringField(doc='Human-readable title')
    slug = StringField(doc='Machine-friendly identifier')
    vars = Field(factory=dict)

    license = LicenseField(
        doc=textwrap.dedent('''
            Identifier of the licence under which content is available.
            Note that Naucse supports only a limited set of licences.''')
    )

    attribution = HTMLListField(doc='Authorship information')

    license_code = LicenseField(
        optional=True,
        doc=textwrap.dedent('''
            Identifier of the licence under which code is available.
            Note that Naucse supports only a limited set of licences.''')
    )

    render_call = ObjectField(RenderCall)

    material = parent_property

    source_file = StringField(optional=True)

    @property
    def session(self):
        return self.material.session

    @property
    def course(self):
        return self.material.course

    @reify
    def _rendered_content(self):
        return self.render_call.call()

    @reify
    def solutions(self):
        solutions = []
        for i, content in enumerate(self._rendered_content.get('solutions', ())):
            solution = Solution.load(
                {'content': content, 'index': i},
                parent=self
            )
            solutions.append(solution)

        return solutions

    @reify
    def css(self):
        css = self._rendered_content.get('css', '')
        return sanitize_stylesheet(css)

    @property
    def modules(self):
        return self._rendered_content.get('modules', {})

    def sanitize_content(self, text):
        def lesson_url(*, lesson, page='index', **kw):
            lesson = self.course.get_material(lesson)
            page = lesson.pages[page]
            return page.get_url(**kw)

        def solution_url(*, solution, **kw):
            # XXX: Can't load Solutions yet, so create a fake
            # one to get the URL
            return Solution(parent=self, index=solution).get_url(**kw)

        def static_url(*, filename, **kw):
            return self.material.static_files[filename].get_url(**kw)

        return sanitize_html(
            text,
            url_for={
                'lesson': lesson_url,
                'solution': solution_url,
                'static': static_url,
            }
        )

    def get_content(self):
        return self.sanitize_content(self._rendered_content['content'])

    def get_edit_info(self):
        source_file = self._rendered_content['source_file']
        if source_file is not None:
            return self.course.repo_info.get_edit_info(source_file)

    def freeze(self):
        self._rendered_content


class Material(Model):
    title = StringField(doc='Human-readable title')
    slug = StringField(
        optional=True, doc='Machine-friendly identifier')
    type = StringField(default='page')
    external_url = UrlField(optional=True)
    pages = DictField(Page, optional=True)
    static_files = DictField(StaticFile, optional=True)

    prev = next = None

    @property
    def session(self):
        if isinstance(self._parent, Session):
            return self._parent
        return None

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
        if isinstance(self._parent, Session):
            return self._parent.course
        if isinstance(self._parent, Course):
            return self._parent
        raise TypeError(self._parent)


class SessionPage(Model):
    slug = StringField(doc='Machine-friendly identifier')

    session = parent_property

    @property
    def course(self):
        return self.session.course


def _construct_time(which):
    def _construct(session, data):
        try:
            value = data[f'{which}_time']
        except KeyError:
            try:
                default_time = session.course.default_time
            except AttributeError:
                return NOTHING
            time = default_time[which]
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
    materials = MaterialListField(Material)
    start_time = DateTimeField(
        optional=True,
        construct=_construct_time('start'),
        doc='Times of day when the session starts.')
    end_time = DateTimeField(
        optional=True,
        construct=_construct_time('end'),
        doc='Times of day when the session ends.')
    source_file = StringField(optional=True)

    course = parent_property

    @property  # XXX: Reify? Load but not export?
    def _materials_by_slug(self):
        return {mat.slug: mat for mat in self.materials if mat.slug}

    def get_material(self, slug):
        return self._materials_by_slug[slug]

    @reify
    def pages(self):
        return {
            'front': SessionPage.load({'slug': 'front'}, parent=self),
            'back': SessionPage.load({'slug': 'back'}, parent=self),
        }

    def freeze(self):
        for page in self.pages.values():
            page.freeze()

    def get_edit_info(self):
        if self.source_file is not None:
            return self.course.repo_info.get_edit_info(self.source_file)


def _max_or_none(sequence):
    return max([m for m in sequence if m is not None], default=NOTHING)

def _min_or_none(sequence):
    return min([m for m in sequence if m is not None], default=NOTHING)


class Course(Model):
    def __init__(self, *args, repo_info, **kwargs):
        self.repo_info = repo_info
        self._frozen = False
        super().__init__(*args, **kwargs)

    title = StringField(doc='Human-readable title')
    slug = StringField(optional=True, doc='Machine-friendly identifier')
    subtitle = StringField(optional=True, doc='Human-readable title')
    vars = Field(factory=dict)
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
    extra_materials = Field(factory=dict, output_only=True)

    source_file = StringField(optional=True)

    # XXX: Are "canonical courses" useful?
    canonical = False

    # XXX: Should the "meta" course be special?
    @property
    def is_meta(self):
        return self.slug == 'courses/meta'

    # XXX: Is course derivation useful?
    derives = StringField(
        optional=True, doc="Course this derives from (deprecated)")
    @property
    def base_course(self):
        key = f'courses/{self.derives}'
        try:
            return self.root.courses[key]
        except KeyError:
            return None


    # XXX: is this subclassing necessary?
    @field(optional=True)
    class default_time(Field):
        '''Times of day when sessions notmally take place. May be null.'''
        def convert(self, instance, data, value):
            return {
                'start': time_from_string(data['default_time']['start']),
                'end': time_from_string(data['default_time']['end']),
            }

    sessions = ListDictField(Session, key_attr='slug', index_key='index',
                             prev_next_attrs=('prev', 'next'))

    start_date = DateField(
        construct=lambda instance, data: _min_or_none(getattr(s, 'date', None) for s in instance.sessions.values()),
        optional=True,
        doc='Date when this starts, or None')
    end_date = DateField(
        construct=lambda instance, data: _max_or_none(getattr(s, 'date', None) for s in instance.sessions.values()),
        optional=True,
        doc='Date when this starts, or None')

    @classmethod
    def load_local(cls, parent, slug, *, repo_info):
        data = naucse_render.get_course(slug, version=1)
        jsonschema.validate(data, get_schema(cls, is_input=True))
        result = cls.load({**data, 'slug': slug}, parent=parent, repo_info=repo_info)
        result.base_path = '.'
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
        try:
            return self.extra_materials[slug]
        except KeyError:
            pass
        if not self._frozen:
            info = naucse_render.get_extra_lesson(slug, vars=self.vars)
            material = Material.load(info, parent=self)
            self.extra_materials[slug] = material
            return material
        raise LookupError(slug)

    def freeze(self):
        for sessions in self.sessions.values():
            sessions.freeze()
        for material in self.extra_materials.values():
            material.freeze()
        self._frozen = True

    def get_edit_info(self):
        if self.source_file is not None:
            return self.repo_info.get_edit_info(self.source_file)

    def get_static_file_info(self, filename):
        return self.base_path, filename


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


class License(Model):
    title = StringField()
    url = UrlField()


class Root(Model):
    courses = DictField(Course)
    run_years = DictField(RunYear)

    def __init__(self, *, url_factories, schema_url_factory):
        self.root = self
        self.url_factories = url_factories
        self.schema_url_factory = schema_url_factory

        self.courses = {}
        self.run_years = {}
        self.licenses = {}

    def load_local(self, path):
        self.licenses = self.load_licenses(path / 'licenses')
        self.repo_info = get_local_repo_info(path)

        for course_path in (path / 'courses').iterdir():
            if (course_path / 'info.yml').is_file():
                slug = 'courses/' + course_path.name
                course = Course.load_local(
                    self, slug, repo_info=self.repo_info,
                )
                course.canonical = True
                self.courses[slug] = course

        for year_path in sorted((path / 'runs').iterdir()):
            if year_path.is_dir():
                year = int(year_path.name)
                run_year = RunYear(year=year, parent=self)
                self.run_years[int(year_path.name)] = run_year
                for course_path in year_path.iterdir():
                    if (course_path / 'info.yml').is_file():
                        slug = f'{year_path.name}/{course_path.name}'
                        course = Course.load_local(
                            self, slug, repo_info=self.repo_info,
                        )
                        run_year.runs[slug] = course

        self.courses['lessons'] = Course.load_local(
            self, 'lessons',
            repo_info=self.repo_info,
        )

        self.edit_info = self.repo_info.get_edit_info('')
        self.runs_edit_info = self.repo_info.get_edit_info('runs')

    def load_licenses(self, path):
        licenses = {}
        for licence_path in path.iterdir():
            with (licence_path / 'info.yml').open() as f:
                info = yaml.safe_load(f)
            licenses[licence_path.name] = License.load(info, parent=self)
        return licenses

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
