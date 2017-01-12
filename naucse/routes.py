import os
from flask import Flask, render_template, url_for, send_from_directory
from flask import abort
from jinja2 import PrefixLoader, FileSystemLoader
from jinja2.exceptions import TemplateNotFound


from naucse.utils import read_yaml


app = Flask('naucsepythoncz')
app.config['TEMPLATES_AUTO_RELOAD'] = True


app.jinja_loader = PrefixLoader({
    'templates': FileSystemLoader(os.path.join(app.root_path, 'naucse/templates')),
    'courses': FileSystemLoader(os.path.join(app.root_path, 'courses'))
})


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


    file = open(template, 'r')
    content = file.read()
    title = info['course'] + ': ' + info['title']

    try:
        if info['style'] == "md":
            return render_template('templates/markdown_page.html', static=lection_static_url, lection=lection_url, title=title, content=content)
        elif info['style'] == "ipynb":
            return render_template('templates/ipython_page.html', static=lection_static_url, lection=lection_url, title=title, content=content)
        else:
            return render_template(template, static=lection_static_url, lection=lection_url)
    except TemplateNotFound:
        abort(404)

    file.close()


# Static files in lectures.
@app.route('/courses/<course>/<lection>/static/<path:path>')
def lection_static(course, lection, path):
    directory = os.path.join(app.root_path, 'courses')
    filename = os.path.join(course, lection, 'static', path)
    return send_from_directory(directory, filename)
