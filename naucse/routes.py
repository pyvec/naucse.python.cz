import os

from flask import Flask, render_template, url_for, send_from_directory
from flask import abort, render_template_string
from jinja2 import PrefixLoader, FileSystemLoader, StrictUndefined, Markup
from jinja2.exceptions import TemplateNotFound
from werkzeug.local import LocalProxy
from markdown import markdown

from naucse import models
from naucse.urlconverters import register_url_converters


app = Flask('naucse')
app.config['TEMPLATES_AUTO_RELOAD'] = True

lesson_template_loader = FileSystemLoader(os.path.join(app.root_path, '..', 'lessons'))


@LocalProxy
def model():
    return models.Root(os.path.join(app.root_path, '..'))

register_url_converters(app, model)

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Index page."""
    return render_template("index.html")


@app.route('/about/')
def about():
    """About page."""
    return render_template("about.html")


@app.route('/runs/')
def runs():
    """Runs page."""
    return render_template("run_list.html",
                           run_years=model.run_years,
                           title="Seznam offline kurzů Pythonu")


@app.route('/courses/')
def courses():
    """Page with listed online courses."""
    return render_template("course_list.html", courses=model.courses,
                           title="Seznam online kurzů Pythonu")


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
                               course=course, plan=course.sessions)
    except TemplateNotFound:
        abort(404)


@app.route('/runs/<run:run>/')
def run_page(run):
    """Run's page."""
    def lesson_url(lesson, *args):
        """Link to the specific lesson."""
        return url_for('run_lesson', run=run, lesson=lesson, *args)

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
            return prev, next
    return None, None


def render_lesson(lesson, page='index', **kwargs):
    def static_url(path):
        return url_for('lesson_static', lesson=lesson, path=path)
    kwargs.setdefault('static', static_url)
    kwargs.setdefault('lesson', lesson)

    if lesson.style == 'md':
        name = lesson.path.joinpath('{}.{}'.format(page, lesson.style))
        try:
            file = lesson.path.joinpath(name).open()
        except FileNotFoundError:
            abort(404)
        with file:
            content = file.read()
        content = Markup(markdown(content))
    else:
        env = app.jinja_env.overlay(loader=lesson_template_loader)
        name = '{}/{}.{}'.format(lesson.slug, page, lesson.style)
        try:
            template = env.get_template(name)
        except TemplateNotFound:
            abort(404)
        content = Markup(template.render(**kwargs))

    kwargs.setdefault('title', lesson.title)
    kwargs.setdefault('content', content)

    return render_template('lesson.html', **kwargs)


@app.route('/runs/<run:run>/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/runs/<run:run>/<lesson:lesson>/<page>/')
def run_lesson(run, lesson, page):
    """Run's lesson page."""

    def lesson_static_url(path):
        """Static in the specific lesson."""
        return url_for('lesson_static', lesson=lesson, path=path)


    def lesson_url(lesson, *args):
        """Link to the specific lesson."""
        return url_for('run_lesson', run=run, lesson=lesson, page=page, *args)

    prv, nxt = prv_nxt_teller(run, lesson)
    title = title='{}: {}'.format(run.title, lesson.title)

    return render_lesson(lesson, page=page, title=title,
                         static=lesson_static_url,
                         lesson_url=lesson_url,
                         nxt=nxt, prv=prv)


@app.route('/lessons/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson:lesson>/<page>/')
def lesson(lesson, page):
    """Lesson page."""
    return render_lesson(lesson, page=page)
