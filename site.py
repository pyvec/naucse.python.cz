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


# Lection page.
@app.route('/courses/<course>/<lection>/')
def course_url(course, lection):
    return render_template("courses/" + course + "/" + lection + "/" + "/index.html")

# Provide static files in lectures.
@app.route('/courses/<course>/<lection>/static/<path:path>')
def course_static(course, lection, path):
    directory = os.path.join(app.root_path, 'courses')
    filename = os.path.join(course, lection, 'static', path)
    return send_from_directory(directory, filename)


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
