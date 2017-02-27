import os

from flask import Flask, render_template, url_for, send_from_directory
from flask import abort, render_template_string, g
from jinja2 import PrefixLoader, FileSystemLoader, StrictUndefined, Markup
from jinja2.exceptions import TemplateNotFound
from werkzeug.local import LocalProxy

from naucse import models
from naucse.urlconverters import register_url_converters
from naucse.markdown_util import convert_markdown


app = Flask('naucse')
app.config['TEMPLATES_AUTO_RELOAD'] = True

lesson_template_loader = FileSystemLoader(os.path.join(app.root_path, '..', 'lessons'))


@LocalProxy
def model():
    return models.Root(os.path.join(app.root_path, '..'))

register_url_converters(app, model)

app.jinja_env.undefined = StrictUndefined


@app.before_request
def set_vars():
    g.vars = {}


@app.route('/')
def index():
    """Index page."""
    return render_template("index.html",
                           page_wip=True)


@app.route('/about/')
def about():
    """About page."""
    return render_template("about.html",
                           page_wip=True)


@app.route('/runs/')
def runs():
    """Runs page."""
    return render_template("run_list.html",
                           run_years=model.run_years,
                           title="Seznam offline kurzů Pythonu",
                           page_wip=True)


@app.route('/courses/')
def courses():
    """Page with listed online courses."""
    return render_template("course_list.html", courses=model.courses,
                           title="Seznam online kurzů Pythonu",
                           page_wip=True)


@app.route('/lessons/<lesson:lesson>/static/<path:path>')
def lesson_static(lesson, path):
    """Static files in lessons."""
    directory = str(lesson.path)
    filename = os.path.join('static', path)
    return send_from_directory(directory, filename)


def title_loader(plan):
    """Loads a dictionary of lessons names."""

    lesson_dict = {}

    for lesson in plan:
        for mat in lesson['materials']:
            lesson_link = "/".join(mat['link'].split("/")[-2:])
            if lesson_link[-3:] != "pdf":
                lesson_type = lesson_link.split("/")[1]
                info_file = read_yaml("lessons/" + lesson_link + "/info.yml")
                lesson_dict[mat['link']] = (lesson_type, info_file['title'])
    return lesson_dict


@app.route('/courses/<course:course>/')
def course_page(course):
    """Course page."""
    try:
        return render_template('course.html',
                               course=course, plan=course.sessions,
                               page_wip=True)
    except TemplateNotFound:
        abort(404)


@app.route('/runs/<run:run>/')
def run(run):
    """Run's page."""
    g.vars = dict(run.vars)

    def lesson_url(lesson, *args, **kwargs):
        """Link to the specific lesson."""
        return url_for('run_page', run=run, lesson=lesson, *args, **kwargs)

    try:
        return render_template('run.html',
                               run=run, plan=run.sessions,
                               title=run.title, lesson_url=lesson_url)
    except TemplateNotFound:
        abort(404)


def prv_nxt_teller(run, lesson):
    """Determine the previous and the next lesson."""
    lessons = [
        material.lesson
        for session in run.sessions.values()
        for material in session.materials
        if material.lesson
    ]
    for prev, current, next in zip([None] + lessons,
                                   lessons,
                                   lessons[1:] + [None]):
        if current.slug == lesson.slug:
            if prev:
                prev = prev.index_page
            if next:
                next = next.index_page
            return prev, next
    return None, None


def lesson_template_or_404(lesson, page):
    env = app.jinja_env.overlay(loader=lesson_template_loader)
    name = '{}/{}.{}'.format(lesson.slug, page.slug, page.style)
    try:
        return env.get_template(name)
    except TemplateNotFound:
        abort(404)


def render_page(page, **kwargs):
    lesson = page.lesson
    def static_url(path):
        return url_for('lesson_static', lesson=lesson, path=path)
    def subpage_url(page_slug):
        return url_for('lesson', lesson=lesson, page=page_slug)
    kwargs.setdefault('static', static_url)
    kwargs.setdefault('subpage_url', subpage_url)
    kwargs.setdefault('lesson', lesson)
    kwargs.setdefault('page', page)

    if page.style == 'md':
        if page.jinja:
            template = lesson_template_or_404(lesson, page)
            content = template.render(**kwargs)
        else:
            try:
                file = page.path.open()
            except FileNotFoundError:
                abort(404)
            with file:
                content = file.read()
        content = Markup(convert_markdown(content))
    else:
        template = lesson_template_or_404(lesson, page)
        content = Markup(template.render(**kwargs))

    kwargs.setdefault('title', page.title)
    kwargs.setdefault('content', content)

    kwargs['prv'] = page.previous_page(kwargs.get('prv'))
    kwargs['nxt'] = page.next_page(kwargs.get('nxt'))

    return render_template('lesson.html', **kwargs)


@app.route('/runs/<run:run>/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/runs/<run:run>/<lesson:lesson>/<page>/')
def run_page(run, lesson, page):
    """Run's lesson page."""

    page = lesson.pages[page]
    g.vars = dict(run.vars)
    g.vars.update(page.vars)

    def lesson_url(lesson, *args, **kwargs):
        """Link to the specific lesson."""
        return url_for('run_page', run=run, lesson=lesson, *args, **kwargs)

    def subpage_url(page_slug):
        return url_for('run_page', run=run, lesson=lesson, page=page_slug)

    prv, nxt = prv_nxt_teller(run, lesson)
    title = title='{}: {}'.format(run.title, page.title)

    return render_page(page=page, title=title,
                       lesson_url=lesson_url,
                       subpage_url=subpage_url,
                       run=run, nxt=nxt, prv=prv,
                       page_wip=not page.license)


@app.route('/lessons/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson:lesson>/<page>/')
def lesson(lesson, page):
    """Lesson page."""
    page = lesson.pages[page]
    g.vars = dict(page.vars)
    return render_page(page=page, page_wip=True)
