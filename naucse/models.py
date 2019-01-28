import datetime
from pathlib import Path
import collections.abc
import re
from fnmatch import fnmatch
import shutil

import dateutil
import yaml
from arca import Task

from naucse.edit_info import get_local_repo_info, get_repo_info
from naucse.converters import Field, register_model, BaseConverter
from naucse.converters import ListConverter, DictConverter
from naucse.converters import KeyAttrDictConverter, ModelConverter
from naucse.converters import dump, load, get_converter, get_schema
from naucse import sanitize
from naucse import arca_renderer
from naucse.logger import logger

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

    def dump(self, value):
        return value

    @classmethod
    def get_schema(cls, context):
        return {'type': 'string', 'format': 'uri'}


models = {}


class Model:
    """Base class for naucse models

    Class attributes:

    `init_arg_names` are names of keyword arguments for `__init__`.
    These are copied to attributes of the same name.

    `parent_attrs` is a tuple of attribute names of the object's parents.
    The first for the parent itself; the subsequent ones are set from the
    parent.

    `model_slug` is a Python identifier used in URLs and fragments. It is set
    automatically by default, but can be overridden or set to None in each
    class.

    `pk_name` is the name that holds a primary key
    """
    init_arg_names = {'parent'}
    parent_attrs = ()
    pk_name = None

    def __init__(self, **kwargs):
        for a in self.init_arg_names:
            setattr(self, a, kwargs[a])
        for p in self.parent_attrs[:1]:
            setattr(self, p, self.parent)
        for p in self.parent_attrs[1:]:
            setattr(self, p, getattr(self.parent, p))
        self.root = self.parent.root

    def __init_subclass__(cls):
        try:
            slug = cls.model_slug
        except AttributeError:
            slug = re.sub('([A-Z])', r'-\1', cls.__name__).lower().lstrip('-')
        cls.model_slug = slug
        models[slug] = cls
        if not hasattr(cls, '_naucse__converter'):
            converter = ModelConverter(
                cls, load_arg_names=cls.init_arg_names, slug=slug,
                extra_fields=[Field(
                    URLConverter(), name='_url', data_key='url', input=False,
                    optional=True,
                    doc="URL for a user-facing page on naucse",
                )],
            )
            converter.get_schema_url=_get_schema_url
            register_model(cls, converter)

    def get_url(self, url_type='web', *, external=False):
        return self.root._url_for(
            type(self), pks=self.get_pks(),
            url_type=url_type, external=external)

    def get_pks(self):
        pk_name = f'{self.model_slug}_{self.pk_name}'
        return {**self.parent.get_pks(), pk_name: getattr(self, self.pk_name)}

    @property
    def _url(self):
        try:
            return self.get_url(external=True)
        except NoURL:
            return None
    @_url.setter
    def _url(self, value):
        return

    def __repr__(self):
        pks = ' '.join(f'{k}={v}' for k, v in self.get_pks().items())
        return f'<{type(self).__qualname__} {pks}>'


def _get_schema_url(instance, *, is_input):
    return instance.root.schema_url_factory(
        type(instance), is_input=is_input, _external=True
    )


def _sanitize_page_content(parent, content):
    """Sanitize HTML for a particular page. Also rewrites URLs."""
    parent_page = getattr(parent, 'page', parent)

    def page_url(*, lesson, page='index', **kw):
        return parent_page.course.get_lesson_url(lesson, page=page)

    def solution_url(*, solution, **kw):
        return parent_page.solutions[int(solution)].get_url(**kw)

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
        return str(value)

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
    pk_name = 'index'
    parent_attrs = 'page', 'lesson', 'course'

    content = Field(
        HTMLFragmentConverter(sanitizer=_sanitize_page_content),
        output=False,
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
            'pattern': '^[^./][^/]+(/[^./][^/]+)*$'
        }


source_file_field = Field(
    RelativePathConverter(),
    name='source_file',
    optional=True,
    doc="Path to a source file containing the page's text, "
        + "relative to the repository root")

@source_file_field.after_load()
def _edit_info(self):
    if self.source_file is None:
        self.edit_info = None
    else:
        self.edit_info = self.course.repo_info.get_edit_info(self.source_file)


class StaticFile(Model):
    """Static file specific to a Lesson
    """
    init_arg_names = {'parent', 'filename'}
    pk_name = 'filename'
    parent_attrs = 'lesson', 'course'

    @property
    def base_path(self):
        return self.course.base_path

    def get_pks(self):
        return {**self.parent.get_pks(), 'filename': self.filename}

    path = Field(RelativePathConverter(), doc="Relative path of the file")


class PageCSSConverter(BaseConverter):
    """Converter for CSS for a Page"""
    def load(self, value):
        return sanitize.sanitize_css(value)

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
    pk_name = 'slug'
    parent_attrs = 'lesson', 'course'

    title = Field(str, doc='Human-readable title')

    attribution = Field(ListConverter(HTMLFragmentConverter()),
                        doc='Lines of attribution, as HTML fragments')
    license = Field(
        LicenseConverter(),
        doc='License slugs. Only approved licenses are allowed.')
    license_code = Field(
        LicenseConverter(), optional=True,
        doc='Slug of licence for code snippets.')

    source_file = source_file_field

    css = Field(
        PageCSSConverter(), optional=True,
        doc="CSS specific to this page. (Subject to restrictions which " +
            "aren't yet finalized.)")

    solutions = Field(
        ListConverter(Solution, index_arg='index'),
        factory=list,
        doc="Solutions to problems that appear on the page.")

    modules = Field(
        DictConverter(str), factory=dict,
        doc='Additional modules as a dict with `slug` key and version values')

    content = Field(
        HTMLFragmentConverter(sanitizer=_sanitize_page_content),
        output=False,
        doc='Content, as HTML')


class Lesson(Model):
    """A lesson – collection of Pages on a single topic
    """
    init_arg_names = {'parent', 'slug'}
    pk_name = 'slug'
    parent_attrs = ('course', )

    static_files = Field(
        DictConverter(StaticFile, key_arg='filename'),
        factory=dict,
        doc="Static files the lesson's content may reference")
    pages = Field(
        DictConverter(Page, key_arg='slug', required={'index'}),
        doc="Pages of content. Used for variants (e.g. a page for Linux and "
            + "another for Windows), or non-essential info (e.g. for "
            + "organizers)")

    @property
    def material(self):
        """The material that contains this page, or None"""
        for session in self.course.sessions.values():
            for material in session.materials:
                if self == material.lesson:
                    return material


class Material(Model):
    """Teaching material, usually a link to a lesson or external page
    """
    parent_attrs = 'session', 'course'
    pk_name = 'slug'

    slug = Field(str, optional=True)
    title = Field(str, optional=True, doc="Human-readable title")
    type = Field(
        str,
        doc="Type of the material (e.g. lesson, homework, cheatsheet, link, "
            + "special). Used for the icon in material lists.")
    external_url = Field(
        URLConverter(), optional=True,
        doc="URL for a link to content that's not a naucse lesson")
    lesson_slug = Field(
        str, optional=True,
        doc="Slug of the corresponding lesson")

    @lesson_slug.after_load()
    def _validate_lesson_slug(self):
        if self.lesson_slug and self.external_url:
            raise ValueError(
                'external_url and lesson_slug are incompatible'
            )

    @property
    def lesson(self):
        """Lesson for this Material, or None"""
        if self.lesson_slug is not None:
            return self.course.lessons[self.lesson_slug]

    def get_url(self, url_type='web', **kwargs):
        # The material has no URL itself; it refers to a lesson, an external
        # resource, or to nothing.
        if self.lesson_slug:
            return self.course.get_lesson_url(self.lesson_slug)
        if url_type != 'web':
            raise NoURLType(url_type)
        if self.external_url:
            return self.external_url
        raise NoURL(self)

    def url_or_none(self, *args, **kwargs):
        try:
            return self.get_url(*args, **kwargs)
        except NoURL:
            return None


class SessionPage(Model):
    """Session-specific page, e.g. the front cover
    """
    init_arg_names = {'parent', 'slug'}
    pk_name = 'slug'
    parent_attrs = 'session', 'course'

    content = Field(
        HTMLFragmentConverter(),
        factory=str,
        doc='Content, as HTML')

    def get_pks(self):
        return {**self.parent.get_pks(), 'page_slug': self.slug}


def set_prev_next(sequence):
    """Set "prev" and "next" attributes of each element of a sequence"""
    sequence = list(sequence)
    for prev, now, next in zip(
        [None] + sequence,
        sequence,
        sequence[1:] + [None],
    ):
        now.prev = prev
        now.next = next


class SessionTimeConverter(BaseConverter):
    """Convert a session time, represented in JSON as string

    May be loaded as a complete datetime, or as just date or None, which need
    to be fixed up using `_combine_session_time`.
    Converted to the full datetime on output.
    """
    def load(self, data):
        try:
            return datetime.datetime.strptime('%Y-%m-%d %H:%M:%S', data)
        except ValueError:
            if data.count(':') == 2:
                time = datetime.datetime.strptime(data, '%H:%M:%s').time()
            else:
                time = datetime.datetime.strptime(data, '%H:%M').time()
            return time.replace(tzinfo=dateutil.tz.gettz(_TIMEZONE))

    def dump(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_schema(cls, context):
        _date_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        if context.is_input:
            _time_re = '[0-9]{1,2}:[0-9]{2}(:[0-9]{2})?'
            pattern = f'^({_date_re} )?{_time_re}$'
        else:
            _time_re = '[0-9]{2}:[0-9]{2}:[0-9]{2}'
            pattern = f'^{_date_re} {_time_re}$'
        return {
            'type': 'string',
            'pattern': pattern,
        }


class DateConverter(BaseConverter):
    """Converter for datetime.date values (as 'YYYY-MM-DD' strings in JSON)"""
    def load(self, data):
        return datetime.datetime.strptime(data, "%Y-%m-%d").date()

    def dump(self, value):
        return str(value)

    def get_schema(self, context):
        return {
            'type': 'string',
            'pattern': r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
            'format': 'date',
        }


class Session(Model):
    """A smaller collection of teaching materials

    Usually used for one meeting of an in-preson course or
    a self-contained section of a longer workshop.
    """
    init_arg_names = {'parent', 'index'}
    pk_name = 'slug'
    parent_attrs = ('course', )

    slug = Field(str)
    title = Field(str, doc="A human-readable session title")
    date = Field(
        DateConverter(), optional=True,
        doc="The date when this session occurs (if it has a set time)",
    )

    description = Field(
        HTMLFragmentConverter(), optional=True,
        doc="Short description of the session.")

    source_file = source_file_field

    materials = Field(
        ListConverter(Material),
        factory=list,
        doc="The session's materials",
    )

    @materials.after_load()
    def _index_materials(self):
        set_prev_next(m for m in self.materials if m.lesson_slug)

    pages = Field(
        DictConverter(SessionPage, key_arg='slug'),
        optional=True,
        doc="The session's cover pages")
    @pages.after_load()
    def _set_pages(self):
        if not self.pages:
            self.pages = {}
        for slug in 'front', 'back':
            if slug not in self.pages:
                page = get_converter(SessionPage).load(
                    {}, slug=slug, parent=self,
                )
                self.pages[slug] = page

    time = Field(
        DictConverter(SessionTimeConverter(), required=['start', 'end']),
        optional=True,
        doc="Time when this session takes place.")

    @time.after_load()
    def _fix_time(self):
        if self.time is None:
            self.time = {}
        else:
            if set(self.time) != {'start', 'end'}:
                raise ValueError('Session time may must have start and end')
        result = {}
        for kind in 'start', 'end':
            time = self.time.get(kind, None)
            if isinstance(time, datetime.datetime):
                result[kind] = time
            elif isinstance(time, datetime.time):
                if self.date:
                    result[kind] = datetime.datetime.combine(self.date, time)
                else:
                    self.time = None
                    return
            elif time is None:
                if self.date and self.course.default_time:
                    result[kind] = datetime.datetime.combine(
                        self.date, self.course.default_time[kind],
                    )
                else:
                    self.time = None
                    return
            else:
                raise TypeError(time)
        self.time = result


class AnyDictConverter(BaseConverter):
    """Converter of any JSON-encodable dict"""
    def load(self, data):
        return data

    def dump(self, value):
        return value

    @classmethod
    def get_schema(cls, context):
        return {'type': 'object'}


def time_from_string(time_string):
    """Get datetime.time object from a 'HH:MM' string"""
    hour, minute = time_string.split(':')
    hour = int(hour)
    minute = int(minute)
    tzinfo = dateutil.tz.gettz(_TIMEZONE)
    return datetime.time(hour, minute, tzinfo=tzinfo)


class TimeIntervalConverter(BaseConverter):
    """Converter for a time interval, as a dict with 'start' and 'end'"""
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
                'start': {'type': 'string', 'pattern': '[0-9]{1,2}:[0-9]{2}'},
                'end': {'type': 'string', 'pattern': '[0-9]{1,2}:[0-9]{2}'},
            },
            'required': ['start', 'end'],
            'additionalProperties': False,
        }


class _LessonsDict(collections.abc.Mapping):
    """Dict of lessons with lazily loaded entries"""
    def __init__(self, course):
        self.course = course

    def __getitem__(self, key):
        try:
            return self.course._lessons[key]
        except KeyError:
            self.course.load_lessons([key])
        return self.course._lessons[key]

    def __iter__(self):
        self.course.freeze()
        return iter(self.course._lessons)

    def __len__(self):
        self.course.freeze()
        return len(self.course._lessons)


class Course(Model):
    """Collection of sessions
    """
    pk_name = 'slug'

    def __init__(
        self, *, parent, slug, repo_info, base_path=None, is_meta=False,
        canonical=False,
    ):
        super().__init__(parent=parent)
        self.repo_info = repo_info
        self.slug = slug
        self.base_path = base_path
        self.is_meta = is_meta
        self.course = self
        self._frozen = False
        self.canonical = canonical

        self._lessons = {}
        self._requested_lessons = set()

    lessons = Field(
        DictConverter(Lesson), input=False, doc="""Lessons""")

    @lessons.default_factory()
    def _default_lessons(self):
        return _LessonsDict(self)

    title = Field(str, doc="""Human-readable title""")
    subtitle = Field(
        str, optional=True,
        doc="Human-readable subtitle, mainly used to distinguish several "
            + "runs of same-named courses.")
    description = Field(
        str, optional=True,
        doc="Short description of the course (about one line).")
    long_description = Field(
        HTMLFragmentConverter(), factory=str,
        doc="Long description of the course (up to several paragraphs).")
    vars = Field(
        AnyDictConverter(), factory=dict,
        doc="Defaults for additional values used for rendering pages")
    place = Field(
        str, optional=True,
        doc="Human-readable description of the venue")
    time_description = Field(
        str, optional=True,
        doc="Human-readable description of the time the course takes place "
            + "(e.g. 'Wednesdays')")

    default_time = Field(
        TimeIntervalConverter(), optional=True,
        doc="Default start and end time for sessions")

    sessions = Field(
        KeyAttrDictConverter(Session, key_attr='slug', index_arg='index'),
        doc="Individual sessions")

    @sessions.after_load()
    def _sessions_after_load(self):
        set_prev_next(self.sessions.values())

        for session in self.sessions.values():
            for material in session.materials:
                if material.lesson_slug:
                    self._requested_lessons.add(material.lesson_slug)

    source_file = source_file_field

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
    def load_local(
        cls, slug, *, parent, repo_info, path='.', canonical=False,
        renderer=naucse_render
    ):
        path = Path(path).resolve()
        data = renderer.get_course(slug, version=1, path=path)
        is_meta = (slug == 'courses/meta')
        result = load(
            cls, data, slug=slug, repo_info=repo_info, parent=parent,
            base_path=path, is_meta=is_meta, canonical=canonical,
        )
        result.repo_info = repo_info
        result.renderer = renderer
        return result

    @classmethod
    def load_remote(cls, slug, *, parent, link_info):
        url = link_info['repo']
        branch = link_info.get('branch', 'master')
        renderer = arca_renderer.Renderer(parent.arca, url, branch)
        return cls.load_local(
            slug, parent=parent, repo_info=get_repo_info(url, branch),
            path=renderer.worktree_path,
            renderer=renderer,
        )

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

    def get_recent_derived_runs(self):
        result = []
        if self.canonical:
            today = datetime.date.today()
            cutoff = today - datetime.timedelta(days=2*30)
            for course in self.root.courses.values():
                if (
                    course.start_date
                    and course.base_course == self
                    and course.end_date > cutoff
                ):
                    result.append(course)
        result.sort(key=lambda course: course.start_date, reverse=True)
        return result

    def get_lesson_url(self, slug, *, page='index', **kw):
        if slug in self._lessons:
            return self._lessons[slug].get_url(**kw)
        if self._frozen:
            return KeyError(slug)
        self._requested_lessons.add(slug)
        return self.root._url_for(
            Page, pks={'page_slug': page, 'lesson_slug': slug,
                       **self.get_pks()}
        )

    def load_lessons(self, slugs):
        if self._frozen:
            raise Exception('course is frozen')
        slugs = set(slugs) - set(self._lessons)
        rendered = self.course.renderer.get_lessons(
            slugs, vars=self.vars, path=self.base_path,
        )
        new_lessons = load(
            DictConverter(Lesson, key_arg='slug'),
            rendered,
            parent=self,
        )
        for slug in slugs:
            try:
                lesson = new_lessons[slug]
            except KeyError:
                raise ValueError(f'{slug} missing from rendered lessons')
            self._lessons[slug] = lesson
            self._requested_lessons.discard(slug)

    def load_all_lessons(self):
        if self._frozen:
            return
        self._requested_lessons.difference_update(self._lessons)
        link_depth = 50
        while self._requested_lessons:
            self._requested_lessons.difference_update(self._lessons)
            if not self._requested_lessons:
                break
            self.load_lessons(self._requested_lessons)
            link_depth -= 1
            if link_depth < 0:
                # Avoid infinite loops in lessons
                raise ValueError(
                    f'Lessons in course {self.slug} are linked too deeply')

    def _has_lesson(self, slug):
        # HACK for getting "canonical lesson" info
        return (
            slug in self.course._lessons
            or slug in self.course._requested_lessons
        )

    def freeze(self):
        if self._frozen:
            return
        self.load_all_lessons()
        self._frozen = True


class AbbreviatedDictConverter(DictConverter):
    """Dict that only shows URLs to its items when dumped"""
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


class RunYear(Model, collections.abc.MutableMapping):
    """Collection of courses given in a specific year

    A RunYear behaves as a dict (slug to Course).
    It should contain all courses that take place in a given year.
    One course may be in multiple RunYears if it doesn't start and end in the
    same calendar year.

    RunYear is just a grouping mechanism. It exists to limit the length of
    API responses.
    Some course slugs include a year in them; that's just for extra
    uniqueness and has nothing to do with RunYear.
    """
    pk_name = 'year'

    _naucse__converter = AbbreviatedDictConverter(Course)
    _naucse__converter.get_schema_url=_get_schema_url

    def __init__(self, year, *, parent=None):
        super().__init__(parent=parent)
        self.year = year
        self.runs = {}

    def __getitem__(self, slug):
        return self.runs[slug]

    def __setitem__(self, slug, course):
        self.runs[slug] = course

    def __delitem__(self, slug):
        del self.runs[slug]

    def __iter__(self):
        # XXX: Sort by ... start date?
        return iter(self.runs)

    def __len__(self):
        return len(self.runs)

    def get_pks(self):
        return {**self.parent.get_pks(), 'year': self.year}


class License(Model):
    """A license for content or code
    """
    init_arg_names = {'parent', 'slug'}
    pk_name = 'slug'

    url = Field(str)
    title = Field(str)

    def get_url(self, *args, **kwargs):
        # A Licence always has an external URL
        return self.url


class Root(Model):
    """Data for the naucse website

    Contains a collection of courses plus additional metadata.
    """
    def __init__(
        self, *,
        url_factories=None,
        schema_url_factory=None,
        arca=None,
        trusted_repo_patterns=(),
    ):
        self.root = self
        self.url_factories = url_factories or {}
        self.schema_url_factory = schema_url_factory
        super().__init__(parent=self)
        self.arca = arca
        self.trusted_repo_patterns = trusted_repo_patterns

        self.courses = {}
        self.run_years = {}
        self.licenses = {}
        self.self_study_courses = {}

        # For pagination of runs
        # XXX: This shouldn't be necessary
        self.explicit_run_years = set()

    pk_name = None

    self_study_courses = Field(
        AbbreviatedDictConverter(Course),
        doc="""Links to "canonical" courses – ones without a time span""")
    run_years = Field(
        AbbreviatedDictConverter(RunYear),
        doc="""Links to courses by year""")
    licenses = Field(
        DictConverter(License),
        doc="""Allowed licenses""")

    def load_local_courses(self, path):
        """Load local courses and lessons from the given path

        Note: Licenses should be loaded before calling load_local_courses,
        otherwise lessons will have no licences to choose from
        """
        self.repo_info = get_local_repo_info(path)

        self_study_course_path = path / 'courses'
        run_path = path / 'runs'
        lesson_path = path / 'lessons'

        if not lesson_path.exists():
            # At least one of 'runs' or 'courses' should exist for any courses
            # to be loaded. But "lessons" needs to exist either way.
            raise FileNotFoundError(lesson_path)

        def _load_local_course(course_path, slug, canonical_if_local=False):
            link_path = course_path / 'link.yml'
            if link_path.is_file():
                with link_path.open() as f:
                    link_info = yaml.safe_load(f)
                checked_url = '{repo}#{branch}'.format(**link_info)
                if any(
                    fnmatch(checked_url, l) for l in self.trusted_repo_patterns
                ):
                    course = Course.load_remote(
                        slug, parent=self, link_info=link_info,
                    )
                    self.add_course(course)
                else:
                    logger.debug(f'Untrusted repo: {checked_url}')
            if (course_path / 'info.yml').is_file():
                course = Course.load_local(
                    slug, parent=self, repo_info=self.repo_info, path=path,
                    canonical=canonical_if_local,
                )
                self.add_course(course)

        if self_study_course_path.exists():
            for course_path in self_study_course_path.iterdir():
                slug = 'courses/' + course_path.name
                _load_local_course(course_path, slug, canonical_if_local=True)

        if run_path.exists():
            for year_path in sorted(run_path.iterdir()):
                if year_path.is_dir():
                    self.explicit_run_years.add(int(year_path.name))
                    for course_path in year_path.iterdir():
                        slug = f'{year_path.name}/{course_path.name}'
                        _load_local_course(course_path, slug)

        self.add_course(Course.load_local(
            'lessons',
            repo_info=self.repo_info,
            canonical=True,
            parent=self,
            path=path,
        ))

        self_study_order_path = self_study_course_path / 'info.yml'
        if self_study_order_path.exists():
            with (path / 'courses/info.yml').open() as f:
                course_info = yaml.safe_load(f)
            self.featured_courses = [
                self.courses[f'courses/{n}'] for n in course_info['order']
            ]

        self.edit_info = self.repo_info.get_edit_info('.')
        self.runs_edit_info = self.repo_info.get_edit_info('runs')
        self.course_edit_info = self.repo_info.get_edit_info('courses')

    def add_course(self, course):
        slug = course.slug
        if slug in self.courses:
            # XXX: Replacing courses is untested
            old = self.courses[slug]
            if old.start_date:
                for year in range(old.start_date.year, old.end_date.year+1):
                    del self.run_years[year][slug]
            else:
                del self.self_study_courses[slug]

        self.courses[slug] = course
        if course.start_date:
            for year in range(course.start_date.year, course.end_date.year+1):
                if year not in self.run_years:
                    run_year = RunYear(year=year, parent=self)
                    self.run_years[year] = run_year
                self.run_years[year][slug] = course
        else:
            self.self_study_courses[slug] = course

    def freeze(self):
        for course in self.courses.values():
            course.freeze()

    def load_licenses(self, path):
        """Add licenses from files in the given path to the model"""
        for licence_path in path.iterdir():
            with (licence_path / 'info.yml').open() as f:
                info = yaml.safe_load(f)
            slug = licence_path.name
            license = get_converter(License).load(info, parent=self, slug=slug)
            self.licenses[slug] = license

    def get_course(self, slug):
        # XXX: RunYears shouldn't be necessary
        if slug == 'lessons':
            return self.courses[slug]
        year, identifier = slug.split('/')
        if year == 'courses':
            return self.courses[slug]
        else:
            return self.run_years[int(year)][slug]

    def get_pks(self):
        return {}

    def _url_for(self, obj_type, pks, url_type='web', *, external=False):
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
        return url_for(**pks, _external=external)
