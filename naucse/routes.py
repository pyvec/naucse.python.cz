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
    plan = read_yaml("courses/" + course + "/plan.yml")

    lesson_dict = {}

    # Load dictionary of lessons names.
    for lesson in plan:
        for mat in lesson['materials']:
            if len(mat['link'].split('/')) != 1:
                the_course = mat['link'].split('/')[0]
                link = mat['link'].split('/')[1]
            else:
                link = mat['link']
                the_course = course
            info_file = read_yaml("courses/" + the_course + "/" + link + "/info.yml")
            lesson_dict[mat['link']] = (the_course, info_file['title'])

    try:
        return render_template(template, plan=read_yaml("courses/" + course + "/plan.yml"), names=lesson_dict)
    except TemplateNotFound:
        abort(404)


# Lesson page.
@app.route('/courses/<course>/<lesson>/', defaults={'page': 'index'})
@app.route('/courses/<course>/<lesson>/<page>/')
def course_lesson(course, lesson, page):
    info = read_yaml("courses/" + course + "/" + lesson + "/info.yml")
    template = 'courses/{}/{}/{}.{}'.format(course, lesson, page, info['style'])


    # Static in the specific lesson.
    def lesson_static_url(path):
        return url_for('lesson_static', course=course, lesson=lesson, path=path)


    # Link to the specific lesson.
    def lesson_url(lesson):
        return url_for('course_lesson', course=course, lesson=lesson, page=page)


    file = open(template, 'r')
    content = file.read()
    title = info['course'] + ': ' + info['title']

    try:
        if info['style'] == "md":
            return render_template('templates/markdown_page.html', static=lesson_static_url, lesson=lesson_url, title=title, content=content)
        elif info['style'] == "ipynb":
            return render_template('templates/ipython_page.html', static=lesson_static_url, lesson=lesson_url, title=title, content=content)
        else:
            return render_template(template, static=lesson_static_url, lesson=lesson_url)
    except TemplateNotFound:
        abort(404)

    file.close()


# Static files in lessons.
@app.route('/courses/<course>/<lesson>/static/<path:path>')
def lesson_static(course, lesson, path):
    directory = os.path.join(app.root_path, 'courses')
    filename = os.path.join(course, lesson, 'static', path)
    return send_from_directory(directory, filename)
