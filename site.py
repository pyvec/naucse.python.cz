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


################################
###### @TEMPLATE_FUNCTION ######

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


########################
###### @APP.ROUTE ######

# Index page.
@app.route('/')
def index():
    return render_template("templates/index.html")


# About page.
@app.route('/about/')
def about():
    return render_template("templates/about.html")


# Page with listed online courses.
@app.route('/courses/')
def courses():
    return render_template("courses/index.html", courses=read_yaml("courses/courses.yml"))


# Course page.
@app.route('/courses/<course>/')
def course_page(course):
    template = 'courses/{}/index.html'.format(course)

    try:
        return render_template(template, plan=read_yaml("courses/" + course + "/plan.yml"))
    except TemplateNotFound:
        abort(404)


# Lection page.
@app.route('/courses/<course>/<lection>/', defaults={'page': 'index'})
@app.route('/courses/<course>/<lection>/<page>/')
def course_lection(course, lection, page):
    info = read_yaml("courses/" + course + "/" + lection + "/info.yml")
    template = 'courses/{}/{}/{}.{}'.format(course, lection, page, info['style'])


    # Static in the specific lection.
    def lection_static_url(path):
        return url_for('lection_static', course=course, lection=lection, path=path)


    # Link to the specific lection.
    def lection_url(lection):
        return url_for('course_lection', course=course, lection=lection, page=page)


    if info['style'] == "md":
        file = open(template, 'r')
        content = file.read()
        title = info['course'] + ': ' + info['title']

        try:
            return render_template('templates/markdown_page.html', static=lection_static_url, lection=lection_url, title=title, content=content)

        except TemplateNotFound:
            abort(404)

        file.close()

    elif info['style'] == "ipynb":
        file = open(template, 'r')
        content = file.read()
        title = info['course'] + ': ' + info['title']

        try:
            return render_template('templates/ipython_page.html', static=lection_static_url, lection=lection_url, title=title, content=content)

        except TemplateNotFound:
            abort(404)

    else:
        try:
            return render_template(template, static=lection_static_url, lection=lection_url)

        except TemplateNotFound:
            abort(404)


# Static files in lectures.
@app.route('/courses/<course>/<lection>/static/<path:path>')
def lection_static(course, lection, path):
    directory = os.path.join(app.root_path, 'courses')
    filename = os.path.join(course, lection, 'static', path)
    return send_from_directory(directory, filename)


###################
###### OTHER ######

# Markdown is working.
@app.template_filter('markdown')
def convert_markdown(text):
    text = textwrap.dedent(text)
    result = jinja2.Markup(markdown(text))

    # Markdown code blocks are translated literally, this solves problem with entities.
    result = result.replace('&amp;', '&').replace('&gt;', '>').replace('&#39;', "'").replace('&#34;', '"').replace('&lt;', '<')
    
    return result


# How to read yaml file.
def read_yaml(filename):
    with open(filename, encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data


if __name__ == '__main__':
    cli(app, base_url='http://naucse.python.cz')
