"""Create or serve the naucse.python.cz website
"""

import sys
if sys.version_info[0] <3 :
    raise RuntimeError('We love Python 3.')

import os

from flask import Flask, render_template, url_for, send_from_directory
from flask import redirect, abort
from elsa import cli
from jinja2 import PrefixLoader, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

app = Flask('naucsepythoncz', template_folder="")
app.config['TEMPLATES_AUTO_RELOAD'] = True


app.jinja_loader = PrefixLoader({
    'templates': FileSystemLoader(os.path.join(app.root_path, 'templates')),
    'courses': FileSystemLoader(os.path.join(app.root_path, 'courses')),
})

def template_function(func):
    app.jinja_env.globals[func.__name__] = func
    return func


@template_function
def course_url(course):
    course = course.rstrip('/')
    return url_for('course_page', course=course)


@template_function
def static(filename):
    return url_for('static', filename=filename)


@app.route('/')
def index():
    return render_template("templates/index.html")


@app.route('/courses/')
def courses():
    # XXX: Better list
    return redirect(url_for('index'))


@app.route('/courses/<course>/', defaults={'page': 'index'})
@app.route('/courses/<course>/<page>/')
def course_page(course, page):
    template = 'courses/{}/{}.html'.format(course, page)
    def course_static(path):
        return url_for('course_static', course=course, path=path)

    try:
        return render_template(template,
                               static=course_static)
    except TemplateNotFound:
        abort(404)


@app.route('/courses/<course>/static/<path:path>')
def course_static(course, path):
    directory = os.path.join(app.root_path, 'courses')
    filename = os.path.join(course, 'static', path)
    return send_from_directory(directory, filename)


if __name__ == '__main__':
    cli(app, base_url='http://naucse.python.cz')
