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
    'lessons': FileSystemLoader(os.path.join(app.root_path, 'lessons'))
})


@app.route('/')
def index():
    """Index page."""
    return render_template("templates/index.html")


@app.route('/about/')
def about():
    """About page."""
    return render_template("templates/about.html")


@app.route('/runs/')
def runs():
    """Runs page."""
    return render_template("runs/index.html", runs=read_yaml("runs/runs.yml"), title="Seznam offline kurzů Pythonu")


@app.route('/courses/')
def courses():
    """Page with listed online courses."""
    return render_template("courses/index.html", courses=read_yaml("courses/courses.yml"), title="Seznam online kurzů Pythonu")


@app.route('/lessons/<lesson_type>/<lesson>/static/<path:path>')
def lesson_static(lesson_type, lesson, path):
    """Static files in lessons."""
    directory = os.path.join(app.root_path, 'lessons')
    filename = os.path.join(lesson_type, lesson, 'static', path)
    return send_from_directory(directory, filename)


def title_loader(plan):
    """Loads a dictionary of lessons names."""

    lesson_dict = {}

    for lesson in plan:
        for mat in lesson['materials']:
            lesson_link = "/".join(mat['link'].split("/")[-2:])
            if lesson_link[-3:] != "pdf":
                lesson_type = lesson_link.split("/")[1]
                info_file = read_yaml("lessons/" + lesson_link + "/info.yml")
                lesson_dict[mat['link']] = (lesson_type, info_file['title'])
    return lesson_dict


@app.route('/courses/<course>/')
def course_page(course):
    """Course page."""
    template = 'courses/{}/index.html'.format(course)
    plan = read_yaml("courses/{}/plan.yml".format(course))
    title = (read_yaml("courses/courses.yml"))[course]['title']

    lesson_dict = title_loader(plan)

    try:
        return render_template(template, plan=plan, names=lesson_dict, title=title)
    except TemplateNotFound:
        abort(404)


@app.route('/runs/<year>/<run>/')
def run_page(year, run):
    """Run page."""
    template = "runs/{}/{}/index.html".format(year, run)
    plan = read_yaml("runs/{}/{}/plan.yml".format(year, run))
    title = (read_yaml("runs/runs.yml"))[int(year)][run]['title']

    lesson_dict = title_loader(plan)

    try:
        return render_template(template, plan=plan, names=lesson_dict, title=title)
    except TemplateNotFound:
        abort(404)


@app.route('/runs/<year>/<run>/<lesson_type>/<lesson>/', defaults={'page': 'index'})
@app.route('/runs/<year>/<run>/<lesson_type>/<lesson>/<page>/')
def run_lesson(year, run, lesson_type, lesson, page):
    """Run's lesson page."""
    info = read_yaml("lessons/{}/{}/info.yml".format(lesson_type, lesson))

    template = 'lessons/{}/{}/{}.{}'.format(lesson_type, lesson, page, info['style'])


    def lesson_static_url(path):
        """Static in the specific lesson."""
        return url_for('lesson_static', lesson_type=lesson_type, lesson=lesson, path=path)


    def lesson_url(lesson):
        """Link to the specific lesson."""
        return url_for('run_lesson', year=year, run=run, lesson_type=lesson.split('/')[0], lesson=lesson.split('/')[1], page=page)


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


@app.route('/lessons/<lesson_type>/<lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson_type>/<lesson>/<page>/')
def lesson(lesson_type, lesson, page):
    """Lesson page."""
    info = read_yaml("lessons/{}/{}/info.yml".format(lesson_type, lesson))

    template = 'lessons/{}/{}/{}.{}'.format(lesson_type, lesson, page, info['style'])


    def lesson_static_url(path):
        """Static in the specific lesson."""
        return url_for('lesson_static', lesson_type=lesson_type, lesson=lesson, path=path)


    def lesson_url(lesson):
        """Link to the specific lesson."""
        return url_for('lesson', lesson_type=lesson.split('/')[0], lesson=lesson.split('/')[1], page=page)


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
