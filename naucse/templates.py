from flask import url_for, g
from jinja2 import Markup

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
def run_url(run):
    return url_for('run', run=run)


@template_function
def lesson_url(lesson, page='index'):
    return url_for('lesson', lesson=lesson, page=page)


@template_function
def session_url(run, session, page='front'):
    return url_for('session_page', run=run, session=session, page=page)


@template_function
def var(name):
    """Return a page variable

    Variables are a mechanism for adapting lesson pages to the course
    or run they're part of.
    """
    return g.vars.get(name)


@template_function
def gnd(m, f, *, both=None):
    """Return `m` or `f` based on the user's grammatical gender

    If the gender is not known, return `both`, or "m/f" if not given.
    """
    gender = var('user-gender')
    if gender == 'm':
        return m
    elif gender == 'f':
        return f
    elif both is None:
        return '{}/{}'.format(m, f)
    else:
        return both


@template_function
def anchor(name):
    return Markup('<a id="{}"></a>').format(name)


class A:
    """Stringifies to "" or "a", depending on user's grammatical gender

    (Note for English speakers: This is needed to form the past participle
    of most verbs, which is quite common in tutorials.)
    """
    def __str__(self):
        return gnd('', 'a')

app.jinja_env.globals['a'] = A()


@template_function
def figure(img, alt):
    t = Markup('''
        <span class="figure">
            <a href="{img}">
                <img src="{img}" alt="{alt}">
            </a>
        </span>
    ''')
    return t.strip().format(img=img, alt=alt)
