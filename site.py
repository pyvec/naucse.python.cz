"""Create or serve the naucse.python.cz website
"""

import sys
if sys.version_info[0] <3 :
    raise RuntimeError('We love Python 3.')

import os
import fnmatch
import urllib.parse

from flask import Flask, render_template, url_for, send_from_directory
from flask import redirect
from flask_frozen import Freezer
import yaml
import jinja2
import markdown
import click

from elsa import cli

app = Flask('naucsepythoncz')
app.config['TEMPLATES_AUTO_RELOAD'] = True

v1_path = os.path.join(app.root_path, 'v1/')

@app.route('/')
def index():
    return render_template("index.html")

freezer = Freezer(app)

if __name__ == '__main__':
    cli(app, freezer=freezer, base_url='http://naucse.python.cz')

