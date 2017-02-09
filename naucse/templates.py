from flask import url_for


from naucse.routes import app
from naucse.filters import convert_markdown


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
def run_url(year, run):
    return url_for('run_page', year=year, run=run)


@template_function
def lesson_url(lesson_type, lesson, page='index'):
    return url_for('lesson', lesson_type=lesson_type, lesson=lesson, page=page)
