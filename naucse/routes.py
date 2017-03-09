import os

from flask import Flask, render_template, url_for, send_from_directory
from flask import abort, render_template_string, g
from jinja2 import PrefixLoader, FileSystemLoader, StrictUndefined, Markup
from jinja2.exceptions import TemplateNotFound
from werkzeug.local import LocalProxy
from collections import namedtuple

from naucse import models
from naucse.urlconverters import register_url_converters
from naucse.markdown_util import convert_markdown


app = Flask('naucse')
app.config['TEMPLATES_AUTO_RELOAD'] = True

lesson_template_loader = FileSystemLoader(os.path.join(app.root_path, '..', 'lessons'))
session_template_loader = FileSystemLoader(os.path.join(app.root_path, '..', 'runs'))


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


@app.route('/courses/<course:course>/')
def course_page(course):
    """Course page."""
    try:
        return render_template('course.html',
                               course=course, plan=course.sessions,
                               page_wip=True)
    except TemplateNotFound:
        abort(404)


@app.route('/<run:run>/')
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
    lessons = [material.lesson for session in run.sessions.values() for material in session.materials if material.lesson]

    Arrow = namedtuple('Arrow', ['link', 'title'])

    sess = None
    for session in run.sessions.values():
        for material in session.materials:
            if str(material.lesson) == str(lesson):
                sess = Arrow(session.slug, session.title)

    prv, nxt = None, None

    for prev, current, next in zip([None] + lessons,
                                   lessons,
                                   lessons[1:] + [None]):
        if current.slug == lesson.slug:
            if prev:
                prv = Arrow(prev.slug, prev.title)
            if next:
                nxt = Arrow(next.slug, next.title)

    return prv, nxt, sess


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

    return render_template('lesson.html', **kwargs)


@app.route('/<run:run>/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/<run:run>/<lesson:lesson>/<page>/')
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

    prv, nxt, sess = prv_nxt_teller(run, lesson)

    title = title='{}: {}'.format(run.title, page.title)

    return render_page(page=page, title=title,
                       lesson_url=lesson_url,
                       subpage_url=subpage_url,
                       run=run, prv=prv, nxt=nxt,
                       sess=sess,
                       page_wip=not page.license)


@app.route('/lessons/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson:lesson>/<page>/')
def lesson(lesson, page):
    """Lesson page."""
    page = lesson.pages[page]
    g.vars = dict(page.vars)
    return render_page(page=page, page_wip=True)


####### SESSION


def session_template_or_404(run, session, page):
    env = app.jinja_env.overlay(loader=session_template_loader)
    name = '{}/sessions/{}/{}.md'.format(run.slug, session, page)
    try:
        return env.get_template(name)
    except TemplateNotFound:
        abort(404)


@app.route('/runs/<run:run>/sessions/<session>/', defaults={'page': 'front'})
@app.route('/runs/<run:run>/sessions/<session>/<page>/')
def session_page(run, session, page):
    """Run's session page."""

    def session_url(session):
        """Link to the specific session."""
        return url_for('session_page', run=run, session=session, page=page)

    template = session_template_or_404(run, session, page)
    content = Markup(template.render())

    md_content = Markup(convert_markdown(content))

    return render_template('session.html', content=md_content, page=page)
