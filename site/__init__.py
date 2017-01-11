import sys
if sys.version_info[0] <3 :
    raise RuntimeError('We love Python 3.')

from elsa import cli

from routes import app
from templates import template_function, static, course_url, lection_url
from filters import convert_markdown
from utils import read_yaml


def main():
    cli(app, base_url='http://naucse.python.cz')
