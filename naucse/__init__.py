import sys
if sys.version_info[0] <3 :
    raise RuntimeError('We love Python 3.')

from elsa import cli

from naucse.routes import app

def main():
    cli(app, base_url='http://naucse.python.cz')
