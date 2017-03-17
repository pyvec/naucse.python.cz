import os

from flask import Flask, render_template, url_for, send_from_directory
from flask import abort, g
from jinja2 import StrictUndefined, Markup
from jinja2.exceptions import TemplateNotFound
from werkzeug.local import LocalProxy

from naucse import models
from naucse.urlconverters import register_url_converters
from naucse.templates import setup_jinja_env


app = Flask('naucse')
app.config['TEMPLATES_AUTO_RELOAD'] = True

setup_jinja_env(app.jinja_env)


@LocalProxy
def model():
    return models.Root(os.path.join(app.root_path, '..'))

register_url_converters(app, model)

app.jinja_env.undefined = StrictUndefined


def template_function(func):
    app.jinja_env.globals[func.__name__] = func
    return func


@template_function
def static(filename):
    return url_for('static', filename=filename)


@template_function
def course_url(course):
    return url_for('course_page', course=course)


@template_function
def run_url(run):
    return url_for('run', run=run)


@template_function
def lesson_url(lesson, page='index'):
    return url_for('lesson', lesson=lesson, page=page)


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


def render_page(page, solution=None, **kwargs):
    lesson = page.lesson

    def static_url(path):
        return url_for('lesson_static', lesson=lesson, path=path)

    try:
        content = page.render_html(
            solution=solution,
            static_url=static_url,
            lesson_url=kwargs.get('lesson_url', lesson_url),
        )
    except FileNotFoundError:
        abort(404)

    kwargs.setdefault('lesson', lesson)
    kwargs.setdefault('page', page)

    if solution is not None:
        content = g.solutions[solution]
        template_name = 'solution.html'
        kwargs.setdefault('solution_number', solution)

        # XXX: Link to fragment
        kwargs['prv'] = page
        kwargs['nxt'] = None
    else:
        template_name = 'lesson.html'

        kwargs['prv'] = page.previous_page(kwargs.get('prv'))
        kwargs['nxt'] = page.next_page(kwargs.get('nxt'))

    kwargs.setdefault('title', page.title)
    kwargs.setdefault('content', content)

    return render_template(template_name, **kwargs)


@app.route('/<run:run>/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/<run:run>/<lesson:lesson>/<page>/')
@app.route('/<run:run>/<lesson:lesson>/<page>/solutions/<int:solution>/')
def run_page(run, lesson, page, solution=None):
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
                       page_wip=not page.license,
                       solution=solution)


@app.route('/lessons/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson:lesson>/<page>/')
@app.route('/lessons/<lesson:lesson>/<page>/solutions/<int:solution>/')
def lesson(lesson, page, solution=None):
    """Lesson page."""
    page = lesson.pages[page]
    g.vars = dict(page.vars)
    return render_page(page=page, page_wip=True, solution=solution)
