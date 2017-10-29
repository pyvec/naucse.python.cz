import os
import datetime
import calendar

from flask import Flask, render_template, url_for, send_from_directory
from flask import abort, redirect
from jinja2 import StrictUndefined
from jinja2.exceptions import TemplateNotFound
from werkzeug.local import LocalProxy
from pathlib import Path

from naucse import models
from naucse.urlconverters import register_url_converters
from naucse.templates import setup_jinja_env, vars_functions


app = Flask('naucse')
app.config['TEMPLATES_AUTO_RELOAD'] = True

setup_jinja_env(app.jinja_env)


_cached_model = None

@LocalProxy
def model():
    """Return the root of the naucse model

    In debug mode (elsa serve), a new model is returned for each requests,
    so changes are picked up.

    In non-debug mode (elsa freeze), a single model is used (and stored in
    _cached_model), so that metadata is only read once.
    """
    global _cached_model
    if _cached_model:
        return _cached_model
    model = models.Root(os.path.join(app.root_path, '..'))
    if not app.config['DEBUG']:
        _cached_model = model
    return model

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
    return url_for('course', course=course)


@template_function
def lesson_url(lesson, page='index', solution=None):
    return url_for('lesson', lesson=lesson, page=page, solution=solution)


@template_function
def session_url(course, session, coverpage='front'):
    return url_for("session_coverpage",
                   course=course,
                   session=session,
                   coverpage=coverpage)


@app.route('/')
def index():
    return render_template("index.html",
                           edit_path=Path("."))


@app.route('/runs/')
def runs():
    return render_template("run_list.html",
                           run_years=model.run_years,
                           title="Seznam offline kurzů Pythonu",
                           today=datetime.date.today(),
                           edit_path=model.runs_edit_path)


@app.route('/courses/')
def courses():
    return render_template("course_list.html",
                           courses=model.courses,
                           title="Seznam online kurzů Pythonu",
                           edit_path=model.courses_edit_path)


@app.route('/lessons/<lesson:lesson>/static/<path:path>')
def lesson_static(lesson, path):
    """Get the endpoint for static files in lessons.

    Args:
        lesson  lesson in which is the file located
        path    path to file in the static folder

    Returns:
        endpoint for the static file
    """
    directory = str(lesson.path)
    filename = os.path.join('static', path)
    return send_from_directory(directory, filename)


@app.route('/<course:course>/')
def course(course):
    def lesson_url(lesson, *args, **kwargs):
        return url_for('course_page', course=course, lesson=lesson, *args, **kwargs)

    recent_runs = []
    if not course.start_date:
        # Build a list of "recent" runs based on this course.
        # By recent we mean: haven't ended yet, or ended up to ~2 months ago
        # (Note: even if naucse is hosted dynamically,
        # it's still beneficial to show recently ended runs.)
        today = datetime.date.today()
        cutoff = today - datetime.timedelta(days=2*30)
        this_year = today.year
        for year, run_year in reversed(course.root.run_years.items()):
            for run in run_year.runs.values():
                if run.base_course is course and run.end_date > cutoff:
                    recent_runs.append(run)
            if year < this_year:
                # Assume no run lasts for more than a year,
                # e.g. if it's Jan 2018, some run that started in 2017 may
                # be included, but don't even look through runs from 2016
                # or earlier.
                break
            recent_runs.sort(key=lambda r: r.start_date, reverse=True)

    try:
        return render_template(
            'course.html',
            course=course,
            plan=course.sessions,
            title=course.title,
            lesson_url=lesson_url,
            recent_runs=recent_runs,
            **vars_functions(course.vars),
            edit_path=course.edit_path)
    except TemplateNotFound:
        abort(404)


def render_page(page, solution=None, vars=None, **kwargs):
    lesson = page.lesson

    def static_url(path):
        return url_for('lesson_static', lesson=lesson, path=path)

    try:
        content = page.render_html(
            solution=solution,
            static_url=static_url,
            lesson_url=kwargs.get('lesson_url', lesson_url),
            vars=vars)
    except FileNotFoundError:
        abort(404)

    kwargs.setdefault('lesson', lesson)
    kwargs.setdefault('page', page)

    if solution is not None:
        template_name = 'solution.html'
        kwargs.setdefault('solution_number', solution)

    else:
        template_name = 'lesson.html'

    kwargs.setdefault('title', page.title)
    kwargs.setdefault('content', content)

    return render_template(template_name, **kwargs, **vars_functions(vars),
                           edit_path=page.edit_path)


@app.route('/<course:course>/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/<course:course>/<lesson:lesson>/<page>/')
@app.route('/<course:course>/<lesson:lesson>/<page>/solutions/<int:solution>/')
def course_page(course, lesson, page, solution=None):
    """Render the html of the given lesson page in the course."""

    for session in course.sessions.values():
        for material in session.materials:
            if (material.type == "page" and
                    material.page.lesson.slug == lesson.slug):
                material = material.subpages[page]
                page = material.page
                nxt = material.next
                prv = material.prev
                break
        else:
            continue
        break
    else:
        page = lesson.pages[page]
        prv = nxt = None

    def lesson_url(lesson, *args, **kwargs):
        return url_for('course_page', course=course, lesson=lesson, *args, **kwargs)

    def subpage_url(page_slug):
        return url_for('course_page', course=course, lesson=lesson, page=page_slug)

    canonical_url = url_for('lesson', lesson=lesson, _external=True)

    title = '{}: {}'.format(course.title, page.title)

    return render_page(page=page, title=title,
                       lesson_url=lesson_url,
                       subpage_url=subpage_url,
                       canonical_url=canonical_url,
                       course=course,
                       solution=solution,
                       vars=course.vars,
                       nxt=nxt, prv=prv,
                       session=session)


@app.route('/lessons/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson:lesson>/<page>/')
@app.route('/lessons/<lesson:lesson>/<page>/solutions/<int:solution>/')
def lesson(lesson, page, solution=None):
    """Render the html of the given lesson page."""
    page = lesson.pages[page]
    return render_page(page=page, solution=solution)


@app.route('/<course:course>/sessions/<session>/', defaults={'coverpage': 'front'})
@app.route('/<course:course>/sessions/<session>/<coverpage>/')
def session_coverpage(course, session, coverpage):
    """Render the session coverpage.

    Args:
        course      course where the session belongs
        session     name of the session
        coverpage   coverpage of the session, front is default

    Returns:
        rendered session coverpage
    """

    session = course.sessions.get(session)

    def lesson_url(lesson, *args, **kwargs):
        return url_for('course_page', course=course, lesson=lesson, *args, **kwargs)

    def session_url(session):
        return url_for("session_coverpage",
                       course=course,
                       session=session,
                       coverpage=coverpage)

    content = session.get_coverpage_content(course, coverpage, app)

    template = "coverpage.html"
    if coverpage == "back":
        template = "backpage.html"

    homework_section = False
    link_section = False
    cheatsheet_section = False
    for mat in session.materials:
        if mat.url_type == "homework":
            homework_section = True
        if mat.url_type == "link":
            link_section = True
        if mat.url_type == "cheatsheet":
            cheatsheet_section = True

    return render_template(template,
                           content=content,
                           session=session,
                           course=course,
                           lesson_url=lesson_url,
                           **vars_functions(course.vars),
                           edit_path=session.get_edit_path(course, coverpage),
                           homework_section=homework_section,
                           link_section=link_section,
                           cheatsheet_section=cheatsheet_section)

@app.route('/<course:course>/calendar/')
def course_calendar(course):
    if not course.start_date:
        abort(404)
    months = []
    year = course.start_date.year
    month = course.start_date.month
    while (year, month) <= (course.end_date.year, course.end_date.month):
        months.append((year, month))
        month += 1
        if month > 12:
            month = 1
            year += 1
    sessions_by_date = {s.date: s for s in course.sessions.values()}
    return render_template('course_calendar.html',
                           edit_path=course.edit_path,
                           course=course,
                           sessions_by_date=sessions_by_date,
                           months=months,
                           calendar=calendar.Calendar())
