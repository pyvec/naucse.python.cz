from flask import url_for


from routes import app
from filters import convert_markdown


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
def lection_url(course, lection, page='index'):
    return url_for('course_lection', course=course, lection=lection, page=page)
