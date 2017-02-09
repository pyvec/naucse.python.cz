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
    'courses': FileSystemLoader(os.path.join(app.root_path, 'courses')),
    'runs': FileSystemLoader(os.path.join(app.root_path, 'runs')),
    'terms': FileSystemLoader(os.path.join(app.root_path, 'terms')),
    'videos': FileSystemLoader(os.path.join(app.root_path, 'videos')),
    'lessons': FileSystemLoader(os.path.join(app.root_path, 'lessons'))
})


# Index page.
@app.route('/')
def index():
    return render_template("templates/index.html")


# About page.
@app.route('/about/')
def about():
    return render_template("templates/about.html")


# Runs page.
@app.route('/runs/')
def runs():
    return render_template("runs/index.html", runs=read_yaml("runs/runs.yml"), title="Seznam offline kurzů Pythonu")


# Page with listed online courses.
@app.route('/courses/')
def courses():
    return render_template("courses/index.html", courses=read_yaml("courses/courses.yml"), title="Seznam online kurzů Pythonu")


# Static files in lessons.
@app.route('/lessons/<lesson_type>/<lesson>/static/<path:path>')
def lesson_static(lesson_type, lesson, path):
    directory = os.path.join(app.root_path, 'courses')
    filename = os.path.join(lesson_type, lesson, 'static', path)
    return send_from_directory(directory, filename)


def title_loader(plan):
    """Loads a dictionary of lessons names."""

    lesson_dict = {}

    for lesson in plan:
        for mat in lesson['materials']:
            lesson_link = mat['link']
            lesson_type = lesson_link.split("/")[1]
            info_file = read_yaml(lesson_link + "/info.yml")
            lesson_dict[mat['link']] = (lesson_type, info_file['title'])
    return lesson_dict


# Course page.
@app.route('/courses/<course>/')
def course_page(course):
    template = 'courses/{}/index.html'.format(course)
    plan = read_yaml("courses/{}/plan.yml".format(course))
    title = (read_yaml("courses/courses.yml"))[course]['title']

    lesson_dict = title_loader(plan)

    try:
        return render_template(template, plan=plan, names=lesson_dict, title=title)
    except TemplateNotFound:
        abort(404)


# Run's page.
@app.route('/runs/<year>/<run>/')
def run_page(year, run):
    template = "runs/{}/{}/index.html".format(year, run)
    plan = read_yaml("runs/{}/{}/plan.yml".format(year, run))
    title = (read_yaml("runs/runs.yml"))[run]['title']

    lesson_dict = title_loader(plan)

    try:
        return render_template(template, plan=plan, names=lesson_dict, title=title)
    except TemplateNotFound:
        abort(404)


# Lesson page.
@app.route('/lessons/<lesson_type>/<lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson_type>/<lesson>/<page>/')
def lesson(lesson_type, lesson, page):
    info = read_yaml("lessons/{}/{}/info.yml".format(lesson_type, lesson))

    template = 'lessons/{}/{}/{}.{}'.format(lesson_type, lesson, page, info['style'])


    # Static in the specific lesson.
    def lesson_static_url(path):
        return url_for('lesson_static', lesson_type=lesson_type, lesson=lesson, path=path)


    # Link to the specific lesson.
    def lesson_url(lesson):
        return url_for('lesson', lesson_type=lesson_type, lesson=lesson, page=page)


    file = open(template, 'r')
    content = file.read()
    title = info['course'] + ': ' + info['title']

    try:
        if info['style'] == "md":
            return render_template('templates/_markdown_page.html', static=lesson_static_url, lesson=lesson_url, title=title, content=content)
        elif info['style'] == "ipynb":
            return render_template('templates/_ipython_page.html', static=lesson_static_url, lesson=lesson_url, title=title, content=content)
        else:
            return render_template(template, static=lesson_static_url, lesson=lesson_url, title=title)
    except TemplateNotFound:
        abort(404)

    file.close()
