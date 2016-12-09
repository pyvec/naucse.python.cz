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
from markdown import markdown
import textwrap
import jinja2
import yaml

app = Flask('naucsepythoncz', template_folder="")
app.config['TEMPLATES_AUTO_RELOAD'] = True


app.jinja_loader = PrefixLoader({
    'templates': FileSystemLoader(os.path.join(app.root_path, 'templates')),
    'courses': FileSystemLoader(os.path.join(app.root_path, 'courses')),
})


def template_function(func):
    app.jinja_env.globals[func.__name__] = func
    return func


# Handling static files in the main dirq.
@template_function
def static(filename):
    return url_for('static', filename=filename)


# Index page.
@app.route('/')
def index():
    return render_template("templates/index.html")


# About page.
@app.route('/about/')
def about():
    return render_template("templates/about.html")


# Online courses page.
@app.route('/courses/')
def courses():
    return render_template("templates/courses.html")


# Course page.
@app.route('/courses/<course>/')
def course(course):
    return render_template("courses/" + course + "/index.html", plan=read_yaml("courses/" + course + "/plan.yml"))


# Course lection
@app.route('/courses/<course>/<lection>/', defaults={'page': 'index'})
@app.route('/courses/<course>/<lection>/<page>')
def course_lection(course, lection, page):
    template = 'courses/{}/{}/{}.html'.format(course, lection, page)


    # Static in the specific lection.
    def course_static(path):
        return url_for('course_static', course=course, lection=lection, path=path)


    # Link to the specific lection.
    def lection_url(lection):
        return url_for('lection_url', course=course, lection=lection, page=page)


    try:
        return render_template(template, static=course_static, lection=lection_url)

    except TemplateNotFound:
        abort(404)


# Provide static files in lectures.
@app.route('/courses/<course>/<lection>/static/<path:path>')
def course_static(course, lection, path):
    directory = os.path.join(app.root_path, 'courses')
    filename = os.path.join(course, lection, 'static', path)
    return send_from_directory(directory, filename)


# Provide lection url.
@app.route('/courses/<course>/<lection>/', defaults={'page': 'index'})
@app.route('/courses/<course>/<lection>/<page>')
def lection_url(course, lection, page):
    directory = os.path.join(app.root_path, 'courses', course, lection)
    return send_from_directory(directory, page)


# Markdown is working.
@app.template_filter('markdown')
def convert_markdown(text):
    text = textwrap.dedent(text)
    result = jinja2.Markup(markdown(text))
    return result


# How to read yaml file.
def read_yaml(filename):
    with open(filename, encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data


if __name__ == '__main__':
    cli(app, base_url='http://naucse.python.cz')
