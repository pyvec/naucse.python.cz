from collections import OrderedDict

import jinja2

from naucse.modelutils import Model, YamlProperty, DataProperty, DirProperty
from naucse.modelutils import reify
from naucse.templates import setup_jinja_env, vars_functions
from naucse.markdown_util import convert_markdown
from naucse.notebook_util import convert_notebook


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

    def _prevnext(self, name, default):
        if name in self.info:
            page_slug = self.info[name]
            if page_slug is None:
                return None
            else:
                return self.lesson.pages[page_slug]
        else:
            return default

    def previous_page(self, default):
        """Return the page before this one, or `default`

        The `default` can be a page from another lesson, for cases the ordering
        is determined by a Course or Run.

        Can return `None` if the page is ecplicitly configured to have
        no previous page.
        """
        return self._prevnext('prev', default)

    def next_page(self, default):
        """Like `previous_page`, but for the next page"""
        return self._prevnext('next', default)

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
                if page != 'index' or solution != None:
                    url += '{}/'.format(page)
                if solution != None:
                    url += '{}/'.format(solution)
                return url

        def default_lesson_url(lesson, page='index'):
            url = '../../{}/'.format(lesson.slug)
            if page != 'index':
                url += ''
            return 'static/{}'.format(path)

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

        if self.style == 'md':
            content = jinja2.Markup(convert_markdown(content))
        elif self.style == 'ipynb':
            content = jinja2.Markup(convert_notebook(content))
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


class Material(Model):
    """A link – either to a lesson, or an external URL"""
    def __init__(self, root, path, info, base_collection):
        super().__init__(root, path)
        self.info = info
        self.base_collection = base_collection

    def __str__(self):
        return self.title

    @reify
    def url(self):
        return self.info['url']

    @reify
    def lesson(self):
        try:
            name = self.info['lesson']
        except KeyError:
            return None
        else:
            return self.root.get_lesson(name, self.base_collection)

    @reify
    def title(self):
        try:
            return self.info['title']
        except KeyError:
            pass
        return self.lesson.title


class Session(Model):
    """An ordered collection of materials"""
    def __init__(self, root, path, info, base_collection=None):
        super().__init__(root, path)
        self.info = info
        self.base_collection = base_collection

    def __str__(self):
        return self.title

    info = YamlProperty()

    title = DataProperty(info)
    slug = DataProperty(info)
    date = DataProperty(info, default=None)

    @reify
    def materials(self):
        return [Material(self.root, self.path, s, self.base_collection)
                for s in self.info['materials']]


def _get_sessions(model, plan, base_collection):
    result = OrderedDict(
        (s['slug'],
            Session(model.root, model.path, s, base_collection))
        for s in plan
    )
    if len(result) != len(set(result)):
        raise ValueError('slugs not unique in {!r}'.format(model))
    return result


class Course(Model):
    """A course – ordered collection of sessions"""
    def __str__(self):
        return self.slug

    info = YamlProperty()

    title = DataProperty(info)
    description = DataProperty(info)
    long_description = DataProperty(info)

    @reify
    def slug(self):
        return self.path.parts[-1]

    @reify
    def sessions(self):
        base_collection = self.info.get('base_collection')
        return _get_sessions(self, self.info['plan'], base_collection)


class Run(Model):
    """A run"""
    def __str__(self):
        return '{} - {}'.format(self.slug, self.title)

    info = YamlProperty()

    title = DataProperty(info)
    subtitle = DataProperty(info)
    description = DataProperty(info)
    long_description = DataProperty(info)
    vars = DataProperty(info)

    @reify
    def sessions(self):
        base_collection = self.info.get('base_collection')
        return _get_sessions(self, self.info['plan'], base_collection)

    @reify
    def slug(self):
        return '/'.join(self.path.parts[-2:])


class RunYear(Model):
    """A year of runs"""
    def __str__(self):
        return self.path.parts[-1]

    runs = DirProperty(Run)


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

    @reify
    def runs(self):
        return {
            (year, slug): run
            for year, run_year in self.run_years.items()
            for slug, run in run_year.runs.items()
        }

    def get_lesson(self, name, base_collection=None):
        if isinstance(name, Lesson):
            return name
        if '/' in name:
            base_collection, name = name.split('/', 2)
        collection = self.collections[base_collection]
        return collection.lessons[name]

    @reify
    def lesson_jinja_env(self):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([str(self.path / 'lessons')]),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
        )
        setup_jinja_env(env)
        return env
