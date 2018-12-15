import datetime
from pathlib import Path
import re

import dateutil
import yaml

from naucse.edit_info import get_local_repo_info, get_repo_info
from naucse.converters import Field, register_model, BaseConverter
from naucse.converters import ListConverter, DictConverter
from naucse.converters import KeyAttrDictConverter, ModelConverter
from naucse.converters import dump, load, get_converter, get_schema
from naucse import sanitize

import naucse_render

# XXX: Different timezones?
_TIMEZONE = 'Europe/Prague'


class NoURL(LookupError):
    """An object's URL could not be found"""

class NoURLType(NoURL):
    """The requested URL type is not available"""


class URLConverter(BaseConverter):
    def load(self, data):
        return sanitize.convert_link('href', data)
        return data

    def dump(self, value):
        return value

    @classmethod
    def get_schema(cls, context):
        return {'type': 'string', 'format': 'uri'}


models = {}
model_slugs = {}


class Model:
    """Base class for naucse models

    Class attributes:

    `init_arg_names` are names of keyword arguments for `__init__`.
    These are copied to attributes of the same name.

    `parent_attrs` is a tuple of attribute names of the object's parents.
    The first for the parent itself; the subsequent ones are set from the
    parent.
    """
    init_arg_names = {'parent'}
    parent_attrs = ()

    def __init__(self, **kwargs):
        for a in self.init_arg_names:
            setattr(self, a, kwargs[a])
        for p in self.parent_attrs[:1]:
            setattr(self, p, self.parent)
        for p in self.parent_attrs[1:]:
            setattr(self, p, getattr(self.parent, p))
        self.root = self.parent.root

    def __init_subclass__(cls):
        slug = re.sub('([A-Z])', r'-\1', cls.__name__).lower().lstrip('-')
        def get_schema_url(instance, *, is_input):
            return instance.root.schema_url_factory(
                cls, is_input=is_input, _external=True
            )
        converter = ModelConverter(
            cls, load_arg_names=cls.init_arg_names, slug=slug,
            get_schema_url=get_schema_url,
        )
        models[slug] = cls
        model_slugs[cls] = slug
        register_model(cls, converter)

    def get_url(self, url_type='web', *, external=False):
        return self.root._url_for(self, url_type=url_type, external=external)

    _url = Field(URLConverter(), data_key='url', input=False,
                 doc="URL for a user-facing page on naucse")
    @_url.default_factory()
    def _get_url(self):
        return self.get_url(external=True)

    _api_url = Field(URLConverter(), data_key='api_url', input=False,
                     doc="URL for API")
    @_api_url.default_factory()
    def _get_api_url(self):
        return self.get_url('api', external=True)


def _sanitize_page_content(parent, content):
    """Sanitize HTML for a particular page. Also rewrites URLs."""
    parent_page = getattr(parent, 'page', parent)

    def page_url(*, lesson, page='index', **kw):
        lesson = parent_page.course.get_lesson_shim(lesson)
        return lesson.pages[page].get_url(**kw)

    def solution_url(*, solution, **kw):
        return SolutionShim(parent=parent_page, index=solution).get_url(**kw)

    def static_url(*, filename, **kw):
        return parent_page.lesson.static_files[filename].get_url(**kw)

    return sanitize.sanitize_html(
        content,
        naucse_urls={
            'page': page_url,
            'solution': solution_url,
            'static': static_url,
        }
    )


class HTMLFragmentConverter(BaseConverter):
    """Converter for a HTML fragment."""
    load_arg_names = {'parent'}

    def __init__(self, *, sanitizer=None):
        self.sanitizer = sanitizer

    def load(self, value, parent):
        if self.sanitizer is None:
            return sanitize.sanitize_html(value)
        return self.sanitizer(parent, value)

    def dump(self, value):
        return value

    @classmethod
    def get_schema(cls, context):
        return {
            'type': 'string',
            'format': 'html-fragment',
        }


class Solution(Model):
    """Solution to a problem on a Page
    """
    init_arg_names = {'parent', 'index'}
    parent_attrs = 'page', 'lesson', 'course'

    content = Field(HTMLFragmentConverter(sanitizer=_sanitize_page_content),
                    doc="The right solution, as HTML")


class RelativePathConverter(BaseConverter):
    """Converter for a relative path, as string"""
    def load(self, data):
        return Path(data)

    def dump(self, value):
        return str(value)

    def get_schema(self, context):
        return {
            'type': 'string',
            'pattern': '^[^./][^/]+(/[^./][^/]+)+$'
        }


class StaticFile(Model):
    """Static file specific to a Lesson
    """
    init_arg_names = {'parent', 'filename'}
    parent_attrs = 'lesson', 'course'

    @property
    def base_path(self):
        return self.course.base_path

    path = Field(RelativePathConverter(), doc="Relative path of the file")


class PageCSSConverter(BaseConverter):
    """Converter for CSS for a Page"""
    def load(self, value):
        return sanitize.sanitize_stylesheet(value)

    def dump(self, value):
        return value

    @classmethod
    def get_schema(cls, context):
        return {
            'type': 'string',
            'contentMediaType': 'text/css',
        }


class LicenseConverter(BaseConverter):
    """Converter for a licence (specified as its slug in JSON)"""
    load_arg_names = {'parent'}

    def load(self, value, parent):
        return parent.root.licenses[value]

    def dump(self, value):
        return value.slug

    @classmethod
    def get_schema(cls, context):
        return {
            'type': 'string',
        }


class Page(Model):
    """One page of teaching text
    """
    init_arg_names = {'parent', 'slug'}
    parent_attrs = 'lesson', 'course'

    title = Field(str, doc='Human-readable title')

    content = Field(HTMLFragmentConverter(sanitizer=_sanitize_page_content),
                    doc='Content, as HTML')
    modules = Field(
        DictConverter(str), factory=dict,
        doc='Additional modules as a dict with `slug` keya and version values')

    attribution = Field(ListConverter(HTMLFragmentConverter()),
                        doc='Lines of attribution, as HTML fragments')
    license = Field(
        LicenseConverter(),
        doc='License slugs. Only approved licenses are allowed.')
    license_code = Field(
        LicenseConverter(), optional=True,
        doc='Slug of licence for code snippets.')

    source_file = Field(
        RelativePathConverter(),
        doc="Path to a source file containing the page's text, "
            + "relative to the repository root")

    @source_file.after_load()
    def _edit_info(self):
        if self.source_file is None:
            self.edit_info = None
        else:
            self.edit_info = self.course.repo_info.get_edit_info(self.source_file)

    css = Field(
        PageCSSConverter(), optional=True,
        doc="CSS specific to this page. (Subject to restrictions which " +
            "aren't yet finalized.)")

    solutions = Field(ListConverter(Solution, index_arg='index'))


class Lesson(Model):
    """A lesson – collection of Pages on a single topic
    """
    init_arg_names = {'parent', 'slug'}
    parent_attrs = ('course', )

    static_files = Field(DictConverter(StaticFile, key_arg='filename'))
    pages = Field(DictConverter(Page, key_arg='slug'))

    @property
    def material(self):
        """Return the material that contains this page, or None"""
        for session in self.course.sessions.values():
            for material in session.materials:
                if self == material.lesson:
                    return material


class SolutionShim:
    """Just enough API to get a Solution URL before the lesson is loaded"""
    def __init__(self, *, index, parent):
        self.index = index
        self.page = parent
        self.lesson = parent.lesson
        self.course = parent.course
        self.root = parent.root

    def get_url(self, *args, **kwargs):
        return self.root._url_for(self, *args, obj_type=Solution, **kwargs)


class PageShim:
    """Just enough API to get a Page URL before the lesson is loaded"""
    def __init__(self, *, slug, parent):
        self.slug = slug
        self.lesson = parent
        self.course = parent.course
        self.root = parent.root

    def get_url(self, *args, **kwargs):
        return self.root._url_for(self, *args, obj_type=Page, **kwargs)


class LessonShim:
    """Just enough API to get a Lesson URL before the lesson is loaded"""
    def __init__(self, *, slug, parent):
        self.slug = slug
        self.course = parent
        self.root = parent.root

        class Pages(dict):
            def __missing__(pages_self, key):
                return PageShim(parent=self, slug=key)
        self.pages = Pages()

    def get_url(self, *args, **kwargs):
        return self.root._url_for(self, *args, obj_type=Lesson, **kwargs)


class Material(Model):
    """Teaching material
    """
    parent_attrs = 'session', 'course'

    slug = Field(str, optional=True)
    title = Field(str, optional=True)
    external_url = Field(URLConverter(), optional=True)
    lesson_slug = Field(str, optional=True)
    type = Field(str)

    @property
    def lesson(self):
        if self.lesson_slug is not None:
            if self.external_url:
                raise ValueError(
                    'external_url and lesson_slug are incompatible'
                )
            return self.course.lessons[self.lesson_slug]

    def get_lesson_shim(self):
        if self.lesson_slug:
            return self.course.get_lesson_shim(self.lesson_slug)

    def get_url(self, url_type='web', **kwargs):
        if self.lesson_slug:
            shim = self.course.get_lesson_shim(self.lesson_slug)
            return shim.get_url(**kwargs)
        if url_type != 'web':
            raise NoURLType(url_type)
        if self.external_url:
            return self.external_url


class SessionPage(Model):
    """Session-specific page, e.g. the front cover
    """
    init_arg_names = {'parent', 'slug'}
    parent_attrs = 'session', 'course'

    slug = Field(str)


def set_prev_next(sequence, *, attr_names=('prev', 'next')):
    sequence = list(sequence)
    prev_attr, next_attr = attr_names
    for prev, now, next in zip(
        [None] + sequence,
        sequence,
        sequence[1:] + [None],
    ):
        setattr(now, prev_attr, prev)
        setattr(now, next_attr, next)


class SessionTimeConverter(BaseConverter):
    def load(self, data):
        try:
            return datetime.datetime.strptime('%Y-%m-%d %H:%M:%S', value)
        except ValueError:
            time = datetime.datetime.strptime('%H:%M:%s', value).time()
            return time.replace(tzinfo=dateutil.tz.gettz(_TIMEZONE))

    def dump(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_schema(cls, context):
        return {
            'type': 'string',
            'pattern': '([0-9]{4}-[0-9]{2}-[0-9]{2} )?[0-9]{2}:[0-9]{2}:[0-9]{2}',
        }


def _combine_session_time(session, kind):
    time = getattr(session, f'{kind}_time')
    course = session.course
    default_time = course.default_time
    if time is None:
        if session.date and course.default_time:
            return datetime.datetime.combine(session.date, default_time[kind])
    elif isinstance(time, datetime.time):
        if session.date:
            return datetime.datetime.combine(session.date, time)
    else:
        return time


class DateConverter(BaseConverter):
    """Converts datetime.date values to 'YYYY-MM-DD' strings."""
    def load(self, data):
        return datetime.datetime.strptime(data, "%Y-%m-%d").date()

    def dump(self, value):
        return str(value)

    def get_schema(self, context):
        return {
            'type': 'string',
            'pattern': r'[0-9]{4}-[0-9]{2}-[0-9]{2}',
            'format': 'date',
        }


class Session(Model):
    """A smaller collection of teaching materials
    """
    init_arg_names = {'parent', 'index'}
    parent_attrs = ('course', )

    slug = Field(str)
    title = Field(str)
    date = Field(DateConverter(), optional=True)

    source_file = Field(str)

    @source_file.after_load()
    def _edit_info(self):
        if self.source_file is None:
            self.edit_info = None
        else:
            self.edit_info = self.course.repo_info.get_edit_info(self.source_file)

    materials = Field(ListConverter(Material))

    @materials.after_load()
    def _index_materials(self):
        set_prev_next(m for m in self.materials if not m.external_url)

    @materials.after_load()
    def pages(self):
        # XXX: These should be in the API
        self.pages = {
            'front': SessionPage(slug='front', parent=self),
            'back': SessionPage(slug='back', parent=self),
        }

    start_time = Field(SessionTimeConverter(), optional=True)
    @start_time.after_load()
    def _combine(self):
        self.start_time = _combine_session_time(self, 'start')

    end_time = Field(SessionTimeConverter(), optional=True)
    @end_time.after_load()
    def _combine(self):
        self.end_time = _combine_session_time(self, 'end')


class AnyDictConverter(BaseConverter):
    def load(self, data):
        return data

    def dump(self, value):
        return value

    @classmethod
    def get_schema(cls, context):
        return {'type': 'object'}


def time_from_string(time_string):
    hour, minute = time_string.split(':')
    hour = int(hour)
    minute = int(minute)
    tzinfo = dateutil.tz.gettz(_TIMEZONE)
    return datetime.time(hour, minute, tzinfo=tzinfo)


class TimeIntervalConverter(BaseConverter):
    def load(self, data):
        return {
            'start': time_from_string(data['start']),
            'end': time_from_string(data['end']),
        }

    def dump(self, value):
        return {
            'start': value['start'].strftime('%H:%M'),
            'end': value['end'].strftime('%H:%M'),
        }

    @classmethod
    def get_schema(cls, context):
        return {
            'type': 'object',
            'properties': {
                'start': {'type': 'string', 'pattern': '[0-9]{2}:[0-9]{2}'},
                'end': {'type': 'string', 'pattern': '[0-9]{2}:[0-9]{2}'},
            }
        }


class Course(Model):
    """Collection of sessions
    """
    def __init__(
        self, *, parent=None, slug, repo_info, base_path, is_meta=False,
    ):
        super().__init__(parent=parent)
        self.repo_info = repo_info
        self.slug = slug
        self.base_path = base_path
        self.is_meta = is_meta
        self._frozen = False

        self.lessons = {}
        self._lesson_shims = {}

    title = Field(str)
    subtitle = Field(str, optional=True)
    description = Field(str, optional=True)
    long_description = Field(str, optional=True)
    vars = Field(AnyDictConverter(), factory=dict)
    place = Field(str, optional=True)
    time = Field(str, optional=True)

    default_time = Field(TimeIntervalConverter(), optional=True)

    sessions = Field(KeyAttrDictConverter(
        Session, key_attr='slug', index_arg='index'))

    @sessions.after_load()
    def _index_sessions(self):
        set_prev_next(self.sessions.values())

    source_file = Field(str)

    @source_file.after_load()
    def _edit_info(self):
        if self.source_file is None:
            self.edit_info = None
        else:
            self.edit_info = self.repo_info.get_edit_info(self.source_file)

    start_date = Field(
        DateConverter(),
        doc='Date when this course starts, or None')

    @start_date.default_factory()
    def _construct(self):
        dates = [getattr(s, 'date', None) for s in self.sessions.values()]
        return min((d for d in dates if d), default=None)

    end_date = Field(
        DateConverter(),
        doc='Date when this course ends, or None')

    @end_date.default_factory()
    def _construct(self):
        dates = [getattr(s, 'date', None) for s in self.sessions.values()]
        return max((d for d in dates if d), default=None)

    @classmethod
    def load_local(cls, slug, *, parent, repo_info, canonical=False):
        data = naucse_render.get_course(slug, version=1)
        is_meta = (slug == 'courses/meta')
        result = load(
            cls, data, slug=slug, repo_info=repo_info, parent=parent,
            base_path=Path('.').resolve(), is_meta=is_meta,
        )
        result.repo_info = repo_info
        result.canonical = canonical
        return result

    default_time = Field(TimeIntervalConverter(), optional=True)

    # XXX: Is course derivation useful?
    derives = Field(
        str, optional=True,
        doc="Slug of the course this derives from (deprecated)")

    @derives.after_load()
    def _set_base_course(self):
        key = f'courses/{self.derives}'
        try:
            self.base_course = self.root.courses[key]
        except KeyError:
            self.base_course = None

    def get_lesson_shim(self, slug):
        try:
            return self.lessons[slug]
        except KeyError:
            if not self._frozen:
                try:
                    return self._lesson_shims[slug]
                except KeyError:
                    self._lesson_shims[slug] = LessonShim(
                        slug=slug, parent=self)
                return self._lesson_shims[slug]
            raise

    def load_lessons(self, slugs):
        slugs = set(slugs) - set(self.lessons)
        rendered = naucse_render.get_lessons(slugs, vars=self.vars)
        new_lessons = load(
            DictConverter(Lesson, key_arg='slug'),
            rendered,
            parent=self,
        )
        self.lessons.update(new_lessons)
        for slug in slugs:
            if slug not in new_lessons:
                raise ValueError(f'{slug} missing from rendered lessons')
            self._lesson_shims.pop(slug, None)

    @derives.after_load()
    def _freeze(self):
        if self._frozen:
            return
        for session in self.sessions.values():
            for material in session.materials:
                material.get_lesson_shim()
        link_depth = 50
        while self._lesson_shims:
            self.load_lessons(self._lesson_shims.keys())
            link_depth -= 1
            if link_depth < 0:
                # Avoid infinite loops in lessons
                raise ValueError(
                    f'Lessons in course {self.slug} are linked too deeply')
        self._frozen = True


class AbbreviatedDictConverter(DictConverter):
    def dump(self, value):
        return {
            key: {'$ref': v.get_url('api', external=True)}
            for key, v in value.items()
        }

    def get_schema(self, context):
        return {
            'type': 'object',
            'additionalProperties': {
                '$ref': '#/definitions/ref',
            },
        }


class RunYear(Model):
    """Collection of courses given in a specific year
    """
    def __init__(self, year, *, parent=None):
        super().__init__(parent=parent)
        self.year = year
        self.runs = {}

    def __iter__(self):
        # XXX: Sort by ... start date?
        return iter(self.runs.values())

    runs = Field(AbbreviatedDictConverter(Course))


class License(Model):
    """A license for content or code
    """
    url = Field(str)
    title = Field(str)


class Root(Model):
    """Data for the naucse website

    Contains a collection of courses plus additional metadata.
    """
    def __init__(self, *, url_factories, schema_url_factory):
        self.root = self
        self.url_factories = url_factories
        self.schema_url_factory = schema_url_factory
        super().__init__(parent=self)

        self.courses = {}
        self.run_years = {}
        self.licenses = {}
        self.canonical_courses = {}

    canonical_courses = Field(AbbreviatedDictConverter(Course))
    run_years = Field(AbbreviatedDictConverter(RunYear))
    licenses = Field(DictConverter(License))

    def load_local(self, path):
        """Load local courses from the given path"""
        self.licenses = self.load_licenses(path / 'licenses')
        self.repo_info = get_local_repo_info(path)

        for course_path in (path / 'courses').iterdir():
            if (course_path / 'info.yml').is_file():
                slug = 'courses/' + course_path.name
                course = Course.load_local(
                    slug, parent=self, repo_info=self.repo_info,
                    canonical=True,
                )
                self.courses[slug] = course
                self.canonical_courses[slug] = course

        for year_path in sorted((path / 'runs').iterdir()):
            if year_path.is_dir():
                year = int(year_path.name)
                run_year = RunYear(year=year, parent=self)
                self.run_years[int(year_path.name)] = run_year
                for course_path in year_path.iterdir():
                    if (course_path / 'info.yml').is_file():
                        slug = f'{year_path.name}/{course_path.name}'
                        course = Course.load_local(
                            slug, parent=self, repo_info=self.repo_info,
                        )
                        run_year.runs[slug] = course
                        self.courses[slug] = course

        self.courses['lessons'] = Course.load_local(
            'lessons',
            repo_info=self.repo_info,
            canonical=True,
            parent=self,
        )

        with (path / 'courses/info.yml').open() as f:
            course_info = yaml.safe_load(f)
        self.featured_courses = [
            self.courses[f'courses/{n}'] for n in course_info['order']
        ]

        self.edit_info = self.repo_info.get_edit_info('')
        self.runs_edit_info = self.repo_info.get_edit_info('runs')
        self.course_edit_info = self.repo_info.get_edit_info('courses')

    def load_licenses(self, path):
        licenses = {}
        for licence_path in path.iterdir():
            with (licence_path / 'info.yml').open() as f:
                info = yaml.safe_load(f)
            license = get_converter(License).load(info, parent=self)
            licenses[licence_path.name] = license
        return licenses

    def runs_from_year(self, year):
        try:
            runs = self.run_years[year].runs
        except KeyError:
            return []
        return list(runs.values())

    def get_course(self, slug):
        # XXX: RunYears shouldn't be necessary
        if slug == 'lessons':
            return self.courses[slug]
        year, identifier = slug.split('/')
        if year == 'courses':
            return self.courses[slug]
        else:
            return self.run_years[int(year)].runs[slug]

    def _url_for(self, obj, url_type='web', *, obj_type=None, external=False):
        try:
            urls = self.url_factories[url_type]
        except KeyError:
            raise NoURLType(url_type)
        if obj_type is None:
            obj_type = type(obj)
        try:
            url_for = urls[obj_type]
        except KeyError:
            raise NoURL(obj_type)
        return url_for(obj, _external=external)
