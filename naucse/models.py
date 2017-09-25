from collections import OrderedDict
import copy

import jinja2

from naucse.modelutils import Model, YamlProperty, DataProperty, DirProperty
from naucse.modelutils import reify
from naucse.templates import setup_jinja_env, vars_functions
from naucse.markdown_util import convert_markdown
from naucse.notebook_util import convert_notebook
from pathlib import Path


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
        return self.info.get('css')

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
        if self.info.get('license') is None:
            return None
        return self.root.licenses[self.info['license']]

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

        kwargs = {
            'static': lambda path: static_url(path),
            'lesson_url': lambda lesson, page='index', solution=None:
                lesson_url(lesson=lesson, page=page, solution=solution),
            'subpage_url': lambda page: lesson_url(lesson=lesson, page=page),
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
        return UrlMaterial(root, path, info["url"], info["title"], info.get("type"))
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

    return _merge_dict(result, patch)


class Session(Model):
    """An ordered collection of materials"""
    def __init__(self, root, path, base_course, info):
        super().__init__(root, path)
        base_name = info.get('base')
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
    for sess_info in plan:
        session = Session(course.root, course.path, course.base_course, sess_info)
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


class Course(Model):
    """A course – ordered collection of sessions"""
    def __str__(self):
        return '{} - {}'.format(self.slug, self.title)

    info = YamlProperty()
    title = DataProperty(info)
    description = DataProperty(info)
    long_description = DataProperty(info)

    vars = DataProperty(info)
    subtitle = DataProperty(info, default=None)
    time = DataProperty(info, default=None)
    place = DataProperty(info, default=None)

    canonical = DataProperty(info, default=False)

    @reify
    def base_course(self):
        name = self.info.get('derives')
        if name is None:
            return None
        return self.root.courses[name]

    @reify
    def slug(self):
        directory = self.path.parts[-1]
        parent_directory = self.path.parts[-2]
        if parent_directory == "courses":
            parent_directory = "course" # legacy URL
        return parent_directory + "/" + directory

    @reify
    def sessions(self):
        return _get_sessions(self, self.info['plan'])

    @reify
    def edit_path(self):
        return self.path.relative_to(self.root.path) / "info.yml"

    @reify
    def start_date(self):
        return min(s.date for s in self.sessions.values() if s.date is not None)

    @reify
    def end_date(self):
        return max(s.date for s in self.sessions.values() if s.date is not None)


class RunYear(Model):
    """A year of runs"""
    def __str__(self):
        return self.path.parts[-1]

    runs = DirProperty(Course)


class License(Model):
    def __str__(self):
        return self.path.parts[-1]

    info = YamlProperty()

    title = DataProperty(info)
    url = DataProperty(info)


class Root(Model):
    """The base of the model"""
    def __init__(self, path):
        super().__init__(self, path)

    collections = DirProperty(Collection, 'lessons')
    courses = DirProperty(Course, 'courses')
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

    def get_lesson(self, name):
        if isinstance(name, Lesson):
            return name
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
