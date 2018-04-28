import os
import re
from collections import OrderedDict
from operator import attrgetter
import datetime

import cssutils
import dateutil.tz
import giturlparse
import jinja2
from arca import Task
from git import Repo

import naucse.utils.views
from naucse.utils.models import Model, YamlProperty, DataProperty, DirProperty, MultipleModelDirProperty, ForkProperty
from naucse.utils.models import reify, arca
from naucse.utils.views import absolute_urls_to_freeze
from naucse.validation import AllowedElementsParser
from naucse.templates import setup_jinja_env, vars_functions
from naucse.utils.markdown import convert_markdown
from naucse.utils.notebook import convert_notebook
from pathlib import Path


_TIMEZONE = 'Europe/Prague'
allowed_elements_parser = AllowedElementsParser()


class Lesson(Model):
    """An individual lesson stored on naucse"""
    def __str__(self):
        return '{} - {}'.format(self.slug, self.title)

    info = YamlProperty()

    title = DataProperty(info)

    @reify
    def slug(self):
        return '/'.join(self.path.parts[-2:])

    @reify
    def pages(self):
        pages = dict(self.info.get('subpages', {}))
        pages.setdefault('index', {})
        return {slug: Page(self, slug, self.info, p)
                for slug, p in pages.items()}

    @reify
    def index_page(self):
        return self.pages['index']


class Page(Model):
    """A (sub-) page of a lesson"""
    def __init__(self, lesson, slug, *infos):
        self.slug = slug
        self.info = {}
        for i in infos:
            self.info.update(i)
        self.lesson = lesson
        path = lesson.path.joinpath('{}.{}'.format(slug, self.info['style']))
        super().__init__(lesson.root, path)

    def __str__(self):
        return '{}/{}'.format(self.lesson.slug, self.slug)

    @reify
    def style(self):
        return self.info['style']

    @reify
    def title(self):
        return self.info['title']

    @reify
    def jinja(self):
        return self.info.get('jinja', True)

    @reify
    def latex(self):
        return self.info.get('latex', False)

    @reify
    def css(self):
        """Return lesson-specific extra CSS.

        If the lesson defines extra CSS, the scope of the styles is limited
        to ``.lesson-content``, which contains the actual lesson content.
        """
        css = self.info.get("css")

        if css is None:
            return None

        return self.limit_css_to_lesson_content(css)

    @reify
    def edit_path(self):
        return self.path.relative_to(self.root.path)

    @reify
    def attributions(self):
        attr = self.info.get('attribution', ())
        if isinstance(attr, str):
            attr = [attr]
        return tuple(attr)

    @reify
    def license(self):
        return self.root.licenses[self.info['license']]

    @reify
    def license_code(self):
        if 'license_code' in self.info:
            return self.root.licenses[self.info['license_code']]
        return None

    @reify
    def vars(self):
        return self.info.get('vars', {})

    def _get_template(self):
        name = '{}/{}.{}'.format(self.lesson.slug, self.slug, self.style)
        try:
            return self.root.lesson_jinja_env.get_template(name)
        except jinja2.TemplateNotFound:
            raise FileNotFoundError(name)

    def render_html(self, solution=None,
                    static_url=None,
                    lesson_url=None,
                    subpage_url=None,
                    vars=None,
                    ):
        lesson = self.lesson

        if not vars:
            vars = {}
        else:
            vars = dict(vars)
        vars.update(self.vars)

        solutions = []

        if static_url is None:
            def static_url(path):
                return 'static/{}'.format(path)

        if lesson_url is None:
            def lesson_url(lesson, page='index', solution=None):
                lesson = self.root.get_lesson(lesson)
                url = '../../{}/'.format(lesson.slug)
                if page != 'index' or solution is not None:
                    url += '{}/'.format(page)
                if solution is not None:
                    url += '{}/'.format(solution)
                return url

        if subpage_url is None:
            def subpage_url(page):
                return lesson_url(lesson=lesson, page=page)

        kwargs = {
            'static': lambda path: static_url(path),
            'lesson_url': lambda lesson, page='index', solution=None:
                lesson_url(lesson=lesson, page=page, solution=solution),
            'subpage_url': subpage_url,
            'lesson': lesson,
            'page': self,
            '$solutions': solutions,
        }
        kwargs.update(vars_functions(vars))

        if self.jinja:
            template = self._get_template()
            content = template.render(**kwargs)
        else:
            with self.path.open() as file:
                content = file.read()

        def convert_url(url):
            prefix = 'static/'
            if not url.startswith(prefix):
                return url
            return static_url(url[len(prefix):])

        if self.style == 'md':
            content = jinja2.Markup(convert_markdown(content, convert_url))
        elif self.style == 'ipynb':
            content = jinja2.Markup(convert_notebook(content, convert_url))
        else:
            template = self._get_template()
            content = jinja2.Markup(content)

        if solution is None:
            return content
        else:
            return solutions[solution]

    @staticmethod
    def limit_css_to_lesson_content(css):
        """Return ``css`` limited just to the ``.lesson-content`` element.

        This doesn't protect against malicious input.
        """
        parser = cssutils.CSSParser(raiseExceptions=True)
        parsed = parser.parseString(css)

        for rule in parsed.cssRules:
            for selector in rule.selectorList:
                # the space is important - there's a difference between for example
                # ``.lesson-content:hover`` and ``.lesson-content :hover``
                selector.selectorText = ".lesson-content " + selector.selectorText

        return parsed.cssText.decode("utf-8")


class Collection(Model):
    """A collection of lessons"""
    def __str__(self):
        return self.path.parts[-1]

    lessons = DirProperty(Lesson)


def material(root, path, info):
    if "lesson" in info:
        lesson = root.get_lesson(info['lesson'])
        page = lesson.pages[info.get("page", "index")]
        return PageMaterial(root, path, page, info.get("type", "lesson"), info.get("title"))
    elif "url" in info:
        url = info["url"]
        if url:
            return UrlMaterial(root, path, url, info["title"], info.get("type"))
        else:
            return SpecialMaterial(root, path, info["title"], info.get("type"))
    else:
        raise ValueError("Unknown material type: {}".format(info))


class Material(Model):
    """A link – either to a lesson, or an external URL"""
    def __init__(self, root, path, url_type):
        super().__init__(root, path)
        self.url_type = url_type
        self.prev = None
        self.next = None
        # prev and next is set later

    def __str__(self):
        return self.title


class PageMaterial(Material):
    type = "page"
    has_navigation = True

    def __init__(self, root, path, page, url_type, title=None, subpages=None):
        super().__init__(root, path, url_type)
        self.page = page
        self.title = title or page.title

        if subpages is None:
            self.subpages = {}

            for slug, subpage in page.lesson.pages.items():
                if slug == self.page.slug:
                    item = self
                else:
                    item = PageMaterial(root, path, subpage, url_type,
                                        subpages=self.subpages)
                self.subpages[slug] = item
        else:
            self.subpages = subpages

    def set_prev_next(self, prev, next):
        for slug, subpage in self.subpages.items():
            if slug == self.page.slug:
                subpage.prev = prev
                subpage.next = next
            else:
                subpage.prev = self
                subpage.next = next


class UrlMaterial(Material):
    prev = None
    next = None
    type = "url"
    has_navigation = False

    def __init__(self, root, path, url, title, url_type):
        super().__init__(root, path, url_type)
        self.url = url
        self.title = title


class SpecialMaterial(Material):
    prev = None
    next = None
    type = "special"
    has_navigation = False

    def __init__(self, root, path, title, url_type):
        super().__init__(root, path, url_type)
        self.title = title


def merge_dict(base, patch):
    """Recursively merge `patch` into `base`

    If a key exists in both `base` and `patch`, then:
    - if the values are dicts, they are merged recursively
    - if the values are lists, the value from `patch` is used,
      but if the string `'+merge'` occurs in the list, it is replaced
      with the value from `base`.
    """

    result = dict(base)

    for key, value in patch.items():
        if key not in result:
            result[key] = value
            continue

        previous = base[key]
        if isinstance(value, dict):
            result[key] = merge_dict(previous, value)
        elif isinstance(value, list):
            result[key] = new = []
            for item in value:
                if item == '+merge':
                    new.extend(previous)
                else:
                    new.append(item)
        else:
            result[key] = value
    return result


def time_from_string(time_string):
    hour, minute = time_string.split(':')
    hour = int(hour)
    minute = int(minute)
    tzinfo = dateutil.tz.gettz(_TIMEZONE)
    return datetime.time(hour, minute, tzinfo=tzinfo)


class Session(Model):
    """An ordered collection of materials"""
    def __init__(self, root, path, base_course, info, index, course=None):
        super().__init__(root, path)
        base_name = info.get('base')
        self.index = index
        self.course = course
        if base_name is None:
            self.info = info
        else:
            base = base_course.sessions[base_name].info
            self.info = merge_dict(base, info)
        # self.prev and self.next are set later

    def __str__(self):
        return self.title

    info = YamlProperty()

    title = DataProperty(info)
    slug = DataProperty(info)
    date = DataProperty(info, default=None)
    description = DataProperty(info, default=None)

    def _time(self, time):
        if self.date and time:
            return datetime.datetime.combine(self.date, time)
        return None

    def _session_time(self, key):
        sesion_time = self.info.get('time')
        if sesion_time:
            return time_from_string(sesion_time[key])
        return None

    @reify
    def has_irregular_time(self):
        """True iff the session has its own start or end time, the course has
        a default start or end time, and either of those does not match."""

        irregular_start = self.course.default_start_time is not None \
            and self._time(self.course.default_start_time) != self.start_time
        irregular_end = self.course.default_end_time is not None \
            and self._time(self.course.default_end_time) != self.end_time
        return irregular_start or irregular_end

    @reify
    def start_time(self):
        session_time = self._session_time('start')
        if session_time:
            return self._time(session_time)
        if self.course:
            return self._time(self.course.default_start_time)
        return None

    @reify
    def end_time(self):
        session_time = self._session_time('end')
        if session_time:
            return self._time(session_time)
        if self.course:
            return self._time(self.course.default_end_time)
        return None

    @reify
    def materials(self):
        materials = [material(self.root, self.path, s)
                     for s in self.info['materials']]
        materials_with_nav = [mat for mat in materials if mat.has_navigation]
        for prev, current, next in zip([None] + materials_with_nav,
                                       materials_with_nav,
                                       materials_with_nav[1:] + [None]
                                       ):
            current.set_prev_next(prev, next)

        return materials

    def get_edit_path(self, run, coverpage):
        coverpage_path = self.path / "sessions" / self.slug / (coverpage + ".md")
        if coverpage_path.exists():
            return coverpage_path.relative_to(self.root.path)

        return run.edit_path

    def get_coverpage_content(self, run, coverpage, app):
        coverpage += ".md"
        q = self.path / 'sessions' / self.slug / coverpage

        try:
            with q.open() as f:
                md_content = f.read()
        except FileNotFoundError:
            return ""

        html_content = convert_markdown(md_content)
        return html_content


def _get_sessions(course, plan):
    result = OrderedDict()
    for index, sess_info in enumerate(plan):
        session = Session(course.root, course.path, course.base_course,
                          sess_info, index=index, course=course)
        result[session.slug] = session

    sessions = list(result.values())

    for prev, current, next in zip([None] + sessions,
                                   sessions,
                                   sessions[1:] + [None]):
        current.prev = prev
        current.next = next

    if len(result) != len(set(result)):
        raise ValueError('slugs not unique in {!r}'.format(course))
    if sessions != sorted(sessions, key=lambda d: d.date or 0):
        raise ValueError('sessions not ordered by date in {!r}'.format(course))
    return result


class CourseMixin:
    """Methods common for both :class:`Course` and :class:`CourseLink`.
    """

    @reify
    def slug(self):
        directory = self.path.parts[-1]
        parent_directory = self.path.parts[-2]
        if parent_directory == "courses":
            parent_directory = "course"  # legacy URL
        return parent_directory + "/" + directory

    @reify
    def is_meta(self):
        return self.info.get("meta", False)

    def is_link(self):
        return isinstance(self, CourseLink)

    @reify
    def is_derived(self):
        return self.base_course is not None


class Course(CourseMixin, Model):
    """A course – ordered collection of sessions"""
    def __str__(self):
        return '{} - {}'.format(self.slug, self.title)

    info = YamlProperty()
    title = DataProperty(info)
    description = DataProperty(info)
    long_description = DataProperty(info)

    # none of the variables are required, so empty ``vars:`` should not be required either
    vars = DataProperty(info, default=(), convert=dict)
    subtitle = DataProperty(info, default=None)
    time = DataProperty(info, default=None)
    place = DataProperty(info, default=None)

    canonical = DataProperty(info, default=False)

    data_filename = "info.yml"  # for MultipleModelDirProperty

    # These two class attributes define what the function
    # ``naucse.utils.forks:course_info`` returns from forks,
    # meaning, the function in the fork looks at these lists
    # that are in the fork and returns those.
    # If you're adding an attribute to these lists, you have to
    # make sure that you provide a default in the CourseLink
    # attribute since existing forks don't contain the value.
    COURSE_INFO = ["title", "description", "vars", "canonical"]
    RUN_INFO = ["title", "description", "start_date", "end_date", "canonical", "subtitle", "derives", "vars",
                "default_start_time", "default_end_time"]

    @property
    def derives(self):
        return self.info.get("derives")

    @reify
    def base_course(self):
        name = self.info.get('derives')
        if name is None:
            return None
        return self.root.courses[name]

    @reify
    def sessions(self):
        return _get_sessions(self, self.info['plan'])

    @reify
    def edit_path(self):
        return self.path.relative_to(self.root.path) / "info.yml"

    @reify
    def start_date(self):
        dates = [s.date for s in self.sessions.values() if s.date is not None]
        if not dates:
            return None
        return min(dates)

    @reify
    def end_date(self):
        dates = [s.date for s in self.sessions.values() if s.date is not None]
        if not dates:
            return None
        return max(dates)

    def _default_time(self, key):
        default_time = self.info.get('default_time')
        if default_time:
            return time_from_string(default_time[key])
        return None

    @reify
    def default_start_time(self):
        return self._default_time('start')

    @reify
    def default_end_time(self):
        return self._default_time('end')


def optional_convert_date(datestr):
    if not datestr:
        return None

    try:
        return datetime.datetime.strptime(datestr, "%Y-%m-%d").date()
    except ValueError:
        return None


def optional_convert_time(timestr):
    if not timestr:
        return None

    try:
        return datetime.datetime.strptime(timestr, "%H:%M:%S").time()
    except ValueError:
        return None


class CourseLink(CourseMixin, Model):
    """A link to a course from a separate git repo.
    """

    link = YamlProperty()
    repo: str = DataProperty(link)
    branch: str = DataProperty(link, default="master")

    info = ForkProperty(repo, branch, entry_point="naucse.utils.forks:course_info",
                        args=lambda instance: [instance.slug])
    title = DataProperty(info)
    description = DataProperty(info)
    start_date = DataProperty(info, default=None, convert=optional_convert_date)
    end_date = DataProperty(info, default=None, convert=optional_convert_date)
    subtitle = DataProperty(info, default=None)
    derives = DataProperty(info, default=None)
    vars = DataProperty(info, default=None)
    canonical = DataProperty(info, default=False)
    default_start_time = DataProperty(info, default=None, convert=optional_convert_time)
    default_end_time = DataProperty(info, default=None, convert=optional_convert_time)

    data_filename = "link.yml"  # for MultipleModelDirProperty

    def __str__(self):
        return 'CourseLink: {} ({})'.format(self.repo, self.branch)

    @reify
    def base_course(self):
        name = self.derives
        if name is None:
            return None
        try:
            return self.root.courses[name]
        except LookupError:
            return None

    def render(self, page_type, *args, **kwargs):
        """Render a page in the fork.

        Check the content and registers URLs to freeze.
        """
        naucse.utils.views.forks_raise_if_disabled()

        task = Task(
            "naucse.utils.forks:render",
            args=[page_type, self.slug] + list(args),
            kwargs=kwargs,
        )
        result = arca.run(self.repo, self.branch, task,
                          reference=Path("."), depth=None)

        if page_type != "calendar_ics" and result.output["content"] is not None:
            allowed_elements_parser.reset_and_feed(result.output["content"])

        if "urls" in result.output:
            # Freeze URLs generated by the code in fork, but only if
            # they start with the slug of the course
            absolute_urls_to_freeze.extend([url for url in result.output["urls"] if url.startswith(f"/{self.slug}/")])

        return result.output

    def render_course(self, **kwargs):
        return self.render("course", **kwargs)

    def render_calendar(self, **kwargs):
        return self.render("calendar", **kwargs)

    def render_calendar_ics(self, **kwargs):
        return self.render("calendar_ics", **kwargs)

    def render_page(self, lesson_slug, page, solution, content_key=None, **kwargs):
        return self.render("course_page", lesson_slug, page, solution, content_key=content_key, **kwargs)

    def render_session_coverpage(self, session, coverpage, **kwargs):
        return self.render("session_coverpage", session, coverpage, **kwargs)

    def lesson_static(self, lesson_slug, path):
        filename = arca.static_filename(self.repo, self.branch, Path("lessons") / lesson_slug / "static" / path,
                                        reference=Path("."), depth=None).resolve()

        return filename.parent, filename.name

    def get_footer_links(self, lesson_slug, page, **kwargs):
        """Return links to previous page, current session and the next page.

        Each link is either a dict with 'url' and 'title' keys or ``None``.

        If :meth:`render_page` fails and a canonical version is in the
        base repo, it's used instead with a warning.
        This method provides the correct footer links for the page,
        since ``sessions`` is not included in the info provided by forks.
        """
        naucse.utils.views.forks_raise_if_disabled()

        task = Task(
            "naucse.utils.forks:get_footer_links",
            args=[self.slug, lesson_slug, page],
            kwargs=kwargs
        )

        result = arca.run(self.repo, self.branch, task, reference=Path("."), depth=None)

        to_return = []

        from naucse.views import logger
        logger.debug(result.output)

        if not isinstance(result.output, dict):
            return None, None, None

        def validate_link(link, key):
            return key in link and isinstance(link[key], str)

        for link_type in "prev_link", "session_link", "next_link":
            link = result.output.get(link_type)

            if isinstance(link, dict) and validate_link(link, "url") and validate_link(link, "title"):
                if link["url"].startswith(f"/{self.slug}/"):
                    absolute_urls_to_freeze.append(link["url"])
                to_return.append(link)
            else:
                to_return.append(None)

        logger.debug(to_return)

        return to_return

    @reify
    def edit_path(self):
        return self.path.relative_to(self.root.path) / "link.yml"


class RunYear(Model):
    """A year of runs"""
    def __str__(self):
        return self.path.parts[-1]

    runs = MultipleModelDirProperty([Course, CourseLink])


class License(Model):
    def __str__(self):
        return self.path.parts[-1]

    info = YamlProperty()

    title = DataProperty(info)
    url = DataProperty(info)


class MetaInfo:
    """Info about the current repository.
    """

    def __str__(self):
        return "Meta Information"

    _default_slug = "pyvec/naucse.python.cz"
    _default_branch = "master"

    @reify
    def slug(self):
        """Return the slug of the repository based on the current branch.

        Returns the default if not on a branch, the branch doesn't
        have a remote, or the remote url can't be parsed.
        """
        from naucse.views import logger

        # Travis CI checks out specific commit, so there isn't an active branch
        if os.environ.get("TRAVIS") and os.environ.get("TRAVIS_REPO_SLUG"):
            return os.environ.get("TRAVIS_REPO_SLUG")

        repo = Repo(".")

        try:
            active_branch = repo.active_branch
        except TypeError:  # thrown if not in a branch
            logger.warning("MetaInfo.slug: There is not active branch")
            return self._default_slug

        try:
            remote_name = active_branch.remote_name
        except ValueError:
            tracking_branch = active_branch.tracking_branch()

            if tracking_branch is None:  # a branch without a remote
                logger.warning("MetaInfo.slug: The branch doesn't have a remote")
                return self._default_slug

            remote_name = tracking_branch.remote_name

        remote_url = repo.remotes[remote_name].url

        parsed = giturlparse.parse(remote_url)

        if hasattr(parsed, "owner") and hasattr(parsed, "repo"):
            return f"{parsed.owner}/{parsed.repo}"

        logger.warning("MetaInfo.slug: The url could not be parsed.")
        logger.debug("MetaInfo.slug: Parsed %s", parsed.__dict__)

        return self._default_slug

    @reify
    def branch(self):
        """Return the active branch name, or 'master' if not on a branch.
        """
        from naucse.views import logger

        # Travis CI checks out specific commit, so there isn't an active branch
        if os.environ.get("TRAVIS") and os.environ.get("TRAVIS_BRANCH"):
            return os.environ.get("TRAVIS_BRANCH")

        repo = Repo(".")

        try:
            return repo.active_branch.name
        except TypeError:  # thrown if not in a branch
            logger.warning("MetaInfo.branch: There is not active branch")
            return self._default_branch


class Root(Model):
    """The base of the model"""
    def __init__(self, path):
        super().__init__(self, path)

    collections = DirProperty(Collection, 'lessons')
    courses = MultipleModelDirProperty([Course, CourseLink], 'courses')
    run_years = DirProperty(RunYear, 'runs', keyfunc=int)
    licenses = DirProperty(License, 'licenses')
    courses_edit_path = Path("courses")
    runs_edit_path = Path("runs")

    @reify
    def runs(self):
        return {
            (year, slug): run
            for year, run_year in self.run_years.items()
            for slug, run in run_year.runs.items()
        }

    @reify
    def safe_runs(self):
        return {
            (year, run.slug): run
            for year, run_year in self.safe_run_years.items()
            for run in run_year
        }

    @reify
    def meta(self):
        return MetaInfo()

    @reify
    def safe_run_years(self):
        # since even the basic info about the forked runs can be broken,
        # we need to make sure the required info is provided.
        # If ``RAISE_FORK_ERRORS`` is set, exceptions are raised here.
        # Otherwise the run is ignored completely.
        safe_years = {}
        for year, run_years in self.run_years.items():
            safe_run_years = []

            for run in run_years.runs.values():
                if not run.is_link():
                    safe_run_years.append(run)
                elif (naucse.utils.views.forks_enabled() and
                      naucse.utils.views.does_course_return_info(run, extra_required=["start_date", "end_date"])):
                    safe_run_years.append(run)

            safe_years[year] = safe_run_years

        return safe_years

    def runs_from_year(self, year):
        """Get all runs started in a given year."""
        run_year = self.safe_run_years.get(year)
        if run_year:
            return sorted(run_year, key=attrgetter('start_date'))
        return []

    def get_lesson(self, name):
        if isinstance(name, Lesson):
            return name
        if name[-1] == "/":
            name = name[:-1]
        collection_name, name = name.split('/', 2)
        collection = self.collections[collection_name]
        return collection.lessons[name]

    @reify
    def lesson_jinja_env(self):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([str(self.path / 'lessons')]),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
        )
        setup_jinja_env(env)
        return env
