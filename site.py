"""Create or serve the naucse.python.cz website
"""

import sys
if sys.version_info[0] <3 :
    raise RuntimeError('We love Python 3.')

import os

from flask import Flask, render_template, url_for, Blueprint
from flask import redirect, abort
from flask_frozen import Freezer
import yaml

from elsa import cli

app = Flask('naucsepythoncz', template_folder="")
app.config['TEMPLATES_AUTO_RELOAD'] = True

COURSES = os.listdir(app.root_path+"/courses/")

# Hacky blueprints for static directories

for course in COURSES:
    blueprint = Blueprint('course_'+course, __name__,
        static_url_path='/courses/'+course+'/static',
        static_folder=app.root_path+"/courses/"+course+"/static")
    app.register_blueprint(blueprint)


def course_url(path):
    path = path.rstrip('/')
    return url_for('course', path=path)

app.jinja_env.globals['course_url'] = course_url

@app.route('/')
def index():
    return render_template("templates/index.html")

@app.route('/courses/<path:path>/')
def course(path):
    template_paths = ["courses/"+path+'.html', "courses/"+path+'/index.html']
    for template_path in template_paths:
        if os.path.exists(os.path.join(app.root_path, template_path)):
            return render_template(template_path)
    
    
    abort(404)

freezer = Freezer(app)

if __name__ == '__main__':
    cli(app, freezer=freezer, base_url='http://naucse.python.cz')

