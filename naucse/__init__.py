import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from naucse.freezer import NaucseFreezer

if sys.version_info[0] <3 :
    raise RuntimeError('We love Python 3.')

from naucse.cli import cli
from naucse.views import app, lesson_static_generator


def main():
    arca_log_path = Path(".arca/arca.log")
    arca_log_path.parent.mkdir(exist_ok=True)
    arca_log_path.touch()

    naucse_log_path = Path(".arca/naucse.log")
    naucse_log_path.touch()

    def get_handler(path, **kwargs):
        handler = RotatingFileHandler(path, **kwargs)
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)

        return handler

    logger = logging.getLogger("arca")
    logger.addHandler(get_handler(arca_log_path, maxBytes=10000, backupCount=0))

    logger = logging.getLogger("naucse")
    logger.addHandler(get_handler(naucse_log_path))

    freezer = NaucseFreezer(app)

    # see the generator for details
    freezer.register_generator(lesson_static_generator)

    cli(app, base_url='https://naucse.python.cz', freezer=freezer)
