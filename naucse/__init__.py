import sys
if sys.version_info[0] <3 :
    raise RuntimeError('We love Python 3.')

from elsa import cli

from naucse.routes import app
from naucse.templates import template_function, static, course_url, lesson_url
from naucse.filters import convert_markdown
from naucse.utils import read_yaml


def main():
    cli(app, base_url='http://naucse.python.cz')
