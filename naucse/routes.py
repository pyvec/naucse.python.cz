import os
from flask import Flask, render_template, url_for, send_from_directory
from flask import abort
from jinja2 import PrefixLoader, FileSystemLoader, StrictUndefined
from jinja2.exceptions import TemplateNotFound
from werkzeug.local import LocalProxy

from naucse import models
from naucse.urlconverters import register_url_converters


app = Flask('naucsepythoncz')
app.config['TEMPLATES_AUTO_RELOAD'] = True


app.jinja_loader = PrefixLoader({
    'templates': FileSystemLoader(os.path.join(app.root_path, 'naucse/templates')),
    'lessons': FileSystemLoader(os.path.join(app.root_path, 'lessons'))
})


@LocalProxy
def model():
    return models.Root(app.root_path)

register_url_converters(app, model)

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Index page."""
    return render_template("templates/index.html")


@app.route('/about/')
def about():
    """About page."""
    return render_template("templates/about.html")


@app.route('/runs/')
def runs():
    """Runs page."""
    return render_template("templates/run_list.html",
                           run_years=model.run_years,
                           title="Seznam offline kurzů Pythonu")


@app.route('/courses/')
def courses():
    """Page with listed online courses."""
    return render_template("templates/course_list.html", courses=model.courses,
                           title="Seznam online kurzů Pythonu")


@app.route('/lessons/<lesson:lesson>/static/<path:path>')
def lesson_static(lesson, path):
    """Static files in lessons."""
    directory = os.path.join(app.root_path, 'lessons')
    filename = os.path.join(lesson.slug, 'static', path)
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
        return render_template('templates/course.html',
                               course=course, plan=course.sessions)
    except TemplateNotFound:
        abort(404)


@app.route('/runs/<run:run>/')
def run_page(run):
    """Run's page."""
    def lesson_url(lesson):
        """Link to the specific lesson."""
        return url_for('run_lesson', run=run, lesson=lesson)

    try:
        return render_template('templates/run.html',
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


@app.route('/runs/<run:run>/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/runs/<run:run>/<lesson:lesson>/<page>/')
def run_lesson(run, lesson, page):
    """Run's lesson page."""
    template = 'lessons/{}/{}.{}'.format(lesson.slug, page, lesson.style)


    def lesson_static_url(path):
        """Static in the specific lesson."""
        return url_for('lesson_static', lesson=lesson, path=path)


    def lesson_url(lesson):
        """Link to the specific lesson."""
        return url_for('run_lesson', run=run, lesson=lesson, page=page)

    prv, nxt = prv_nxt_teller(run, lesson)

    with open(template, 'r') as file:
        content = file.read()
    title = '{}: {}'.format(run.title, lesson.title)

    try:
        if lesson.style == "md":
            return render_template('templates/_markdown_page.html', static=lesson_static_url, lesson=lesson_url, title=title, content=content, nxt=nxt, prv=prv)
        elif lesson.style == "ipynb":
            return render_template('templates/_ipython_page.html', static=lesson_static_url, lesson=lesson_url, title=title, content=content, nxt=nxt, prv=prv)
        else:
            return render_template(template, static=lesson_static_url, lesson=lesson_url, title=title, nxt=nxt, prv=prv)
    except TemplateNotFound:
        abort(404)


@app.route('/lessons/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson:lesson>/<page>/')
def lesson(lesson, page):
    """Lesson page."""
    template = 'lessons/{}/{}.{}'.format(lesson.slug, page, lesson.style)

    def lesson_static_url(path):
        """Static in the specific lesson."""
        return url_for('lesson_static', lesson=lesson, path=path)


    def lesson_url(lesson, page='index'):
        """Link to the specific lesson."""
        return url_for('lesson', lesson=lesson, page=page)

    title = lesson.title

    with open(template, 'r') as file:
        content = file.read()

    try:
        if lesson.style == "md":
            return render_template('templates/_markdown_page.html', static=lesson_static_url, lesson=lesson_url, title=title, content=content)
        elif lesson.style == "ipynb":
            return render_template('templates/_ipython_page.html', static=lesson_static_url, lesson=lesson_url, title=title, content=content)
        else:
            return render_template(template, static=lesson_static_url, lesson=lesson_url, title=title)
    except TemplateNotFound:
        abort(404)
