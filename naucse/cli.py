import elsa

from naucse.views import app


def main():
    # XXX: Arca stuff
    elsa.cli(app, base_url='https://naucse.python.cz')
