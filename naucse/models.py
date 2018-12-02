import datetime
from pathlib import Path

import jsonschema
import dateutil
import yaml

from naucse.edit_info import get_local_repo_info, get_repo_info
from naucse.converters import Registry, Field, loader, BaseConverter
from naucse.converters import ListConverter, DictConverter
from naucse.converters import KeyAttrDictConverter
from naucse import sanitize

import naucse_render

# XXX: Different timezones?
_TIMEZONE = 'Europe/Prague'

reg = Registry()

dump = reg.dump


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
    def get_schema(cls):
        return {'type': 'string', 'format': 'uri'}


class Model:
    init_args = {'parent'}
    parent_attrs = ()

    def __init__(self, **kwargs):
        for a in self.init_args:
            setattr(self, a, kwargs[a])
        for p in self.parent_attrs[:1]:
            setattr(self, p, self.parent)
        for p in self.parent_attrs[1:]:
            setattr(self, p, getattr(self.parent, p))
        self.root = self.parent.root

    def __init_subclass__(cls):
        reg.register_model(cls, init_args=cls.init_args)

    def get_url(self, url_type='web', *, external=False):
        return self.root._url_for(self, url_type=url_type, external=external)


def _sanitize_page_content(parent, content):
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
    init_args = {'parent'}

    def __init__(self, *, sanitizer=None):
        self.sanitizer = sanitizer

    def load(self, value, parent):
        if self.sanitizer is None:
            return sanitize.sanitize_html(value)
        return self.sanitizer(parent, value)

    def dump(self, value):
        return value

    @classmethod
    def get_schema(cls):
        return {
            'type': 'string',
            'format': 'html-fragment',
        }


class Solution(Model):
    """Solution to a problem on a Page
    """
    init_args = {'parent', 'index'}
    parent_attrs = 'page', 'lesson', 'course'

    content = Field(HTMLFragmentConverter(sanitizer=_sanitize_page_content))


class StaticFile(Model):
    """Static file specific to a Lesson
    """
    init_args = {'parent', 'filename'}
    parent_attrs = 'lesson', 'course'

    @property
    def base_path(self):
        return self.course.base_path

    path = Field(reg[str])


class PageCSSConverter(BaseConverter):
    def load(self, value):
        return sanitize.sanitize_stylesheet(value)

    def dump(self, value):
        return value

    @classmethod
    def get_schema(cls):
        return {
            'type': 'string',
            'contentMediaType': 'text/css',
        }


class LicenseConverter(BaseConverter):
    init_args = {'parent'}

    def load(self, value, parent):
        return parent.root.licenses[value]

    def dump(self, value):
        return value.slug

    @classmethod
    def get_schema(cls):
        return {
            'type': 'string',
        }


class Page(Model):
    """One page of teaching text
    """
    init_args = {'parent', 'slug'}
    parent_attrs = 'lesson', 'course'

    title = Field(reg[str])

    content = Field(HTMLFragmentConverter(sanitizer=_sanitize_page_content))
    modules = Field(DictConverter(reg[str]), factory=dict)

    attribution = Field(ListConverter(HTMLFragmentConverter()))
    license = Field(LicenseConverter())
    license_code = Field(LicenseConverter(), optional=True)

    source_file = Field(reg[str])

    @source_file.after_load()
    def _edit_info(self):
        if self.source_file is None:
            self.edit_info = None
        else:
            self.edit_info = self.course.repo_info.get_edit_info(self.source_file)

    css = Field(PageCSSConverter(), optional=True)

    @property
    def material(self):
        # XXX
        try:
            for session in self.course.sessions.values():
                for material in session.materials:
                    if self.lesson == material.lesson:
                        return material
        except Exception as e:
            raise ValueError(e)

    solutions = Field(ListConverter(reg[Solution], index_arg='index'))


class Lesson(Model):
    """A lesson – collection of Pages on a single topic
    """
    init_args = {'parent', 'slug'}
    parent_attrs = ('course', )

    static_files = Field(DictConverter(reg[StaticFile], key_arg='filename'))
    pages = Field(DictConverter(reg[Page], key_arg='slug'))


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


class Material(Model):
    """Teaching material
    """
    parent_attrs = 'session', 'course'

    slug = Field(reg[str], optional=True)
    title = Field(reg[str], optional=True)
    external_url = Field(URLConverter(), optional=True)
    lesson_slug = Field(reg[str], optional=True)
    type = Field(reg[str])

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
    parent_attrs = 'session', 'course'

    slug = Field(reg[str])


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
            return datetime.datetime.strftime('%Y-%m-%d %H:%M:%S', value)
        except ValueError:
            time = datetime.datetime.strftime('%H:%M:%s', value).time()
            return time.replace(tzinfo=dateutil.tz.gettz(_TIMEZONE))

    def dump(self, value):
        return value.strptime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_schema(cls):
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


class Session(Model):
    """A smaller collection of teaching materials
    """
    init_args = {'parent', 'index'}
    parent_attrs = ('course', )

    slug = Field(reg[str])
    title = Field(reg[str])
    date = Field(reg[datetime.date], optional=True)

    materials = Field(ListConverter(reg[Material]))

    @materials.after_load()
    def _index_materials(self):
        set_prev_next(m for m in self.materials if not m.external_url)

    source_file = Field(reg[str])

    @source_file.after_load()
    def _edit_info(self):
        if self.source_file is None:
            self.edit_info = None
        else:
            self.edit_info = self.course.repo_info.get_edit_info(self.source_file)

    @loader()
    def pages(self):
        # XXX: These should be in the API
        return {
            'front': reg.load(SessionPage, {'slug': 'front'}, parent=self),
            'back': reg.load(SessionPage, {'slug': 'back'}, parent=self),
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
    def get_schema(cls):
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
            'start': value.strftime('%H:%M'),
            'end': value.strftime('%H:%M'),
        }

    @classmethod
    def get_schema(cls):
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

    title = Field(reg[str])
    subtitle = Field(reg[str], optional=True)
    description = Field(reg[str], optional=True)
    long_description = Field(reg[str], optional=True)
    vars = Field(AnyDictConverter(), factory=dict)
    place = Field(reg[str], optional=True)
    time = Field(reg[str], optional=True)

    default_time = Field(TimeIntervalConverter(), optional=True)

    sessions = Field(KeyAttrDictConverter(
        reg[Session], key_attr='slug', index_arg='index'))

    @sessions.after_load()
    def _index_sessions(self):
        set_prev_next(self.sessions.values())

    source_file = Field(reg[str])

    @source_file.after_load()
    def _edit_info(self):
        if self.source_file is None:
            self.edit_info = None
        else:
            self.edit_info = self.repo_info.get_edit_info(self.source_file)

    start_date = Field(
        reg[datetime.date],
        doc='Date when this course starts, or None')

    @start_date.default_factory()
    def _construct(self):
        dates = [getattr(s, 'date', None) for s in self.sessions.values()]
        return min((d for d in dates if d), default=None)

    end_date = Field(
        reg[datetime.date],
        doc='Date when this course ends, or None')

    @end_date.default_factory()
    def _construct(self):
        dates = [getattr(s, 'date', None) for s in self.sessions.values()]
        return max((d for d in dates if d), default=None)

    @classmethod
    def load_local(cls, slug, *, parent, repo_info, canonical=False):
        data = naucse_render.get_course(slug, version=1)
        jsonschema.validate(data, reg.get_schema(cls))
        is_meta = (slug == 'courses/meta')
        result = reg[cls].load(
            data, slug=slug, repo_info=repo_info, parent=parent,
            base_path=Path('.').resolve(), is_meta=is_meta,
        )
        result.repo_info = repo_info
        result.canonical = canonical
        return result

    default_time = Field(TimeIntervalConverter(), optional=True)

    # XXX: Is course derivation useful?
    derives = Field(
        reg[str], optional=True,
        doc="Course this derives from (deprecated)")

    @loader()
    def base_course(self):
        key = f'courses/{self.derives}'
        try:
            return self.root.courses[key]
        except KeyError:
            return None

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
        for slug, data in rendered.items():
            self.lessons[slug] = reg.load(Lesson, data, parent=self, slug=slug)
            self._lesson_shims.pop(slug, None)

    @loader()
    def _frozen(self):
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
        return True


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


class License(Model):
    """A license for content or code
    """
    url = Field(reg[str])
    title = Field(reg[str])


class Root(Model):
    """Data for the naucse website

    Contains a collection of courses plus additional metadata.
    """
    def __init__(self, *, url_factories, schema_url_factory):
        self.root = self
        super().__init__(parent=self)
        self.root = self
        self.url_factories = url_factories
        self.schema_url_factory = schema_url_factory

        self.courses = {}
        self.run_years = {}
        self.licenses = {}

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
            licenses[licence_path.name] = reg[License].load(info, parent=self)
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
