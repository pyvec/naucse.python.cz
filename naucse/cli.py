import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

import click
import elsa

from naucse.utils.views import forks_enabled, does_course_return_info
from naucse.views import app, lesson_static_generator

from naucse.freezer import NaucseFreezer


def cli(app, *, base_url=None, freezer=None):
    """Return the elsa CLI extended with naucse-specific commands.
    """
    elsa_group = elsa.cli(app, base_url=base_url, freezer=freezer, invoke_cli=False)

    @click.group()
    def naucse():
        pass

    @naucse.command()
    @click.option("--forks-only", default=False, is_flag=True,
                  help="Only list courses and runs from forks")
    def list_courses(forks_only):
        """List all courses and runs and info about them.

        Mainly useful for courses from forks.
        Shows where they are sourced from and if they return even the
        most basic information and will therefore be included in
        list of courses/runs.

        A practical benefit is that on Travis CI, the docker images are
        pulled/built by this command, so freezing won't timeout after
        the 10 minute limit if things are taking particularly long.
        """
        from naucse.views import model

        def canonical(course, suffix=""):
            click.echo(f"  {course.slug}: {course.title}{suffix}")

        def fork_invalid(course):
            click.echo(f"  {course.slug}, from {course.repo}@{course.branch}: "
                       f"Fork doesn't return basic info, will be ignored.")

        def fork_valid(course, suffix=""):
            click.echo(f"  {course.slug}, from {course.repo}@{course.branch}: {course.title}{suffix}")

        click.echo(f"Courses:")

        for course in model.courses.values():
            if forks_only and not course.is_link():
                continue

            if not course.is_link():
                canonical(course)
            elif forks_enabled():
                if does_course_return_info(course, force_ignore=True):
                    fork_valid(course)
                else:
                    fork_invalid(course)

        click.echo(f"Runs:")

        for course in model.runs.values():
            if forks_only and not course.is_link():
                continue

            if not course.is_link():
                canonical(course, suffix=f" ({course.start_date} - {course.end_date})")
            elif forks_enabled():
                if does_course_return_info(course, ["start_date", "end_date"], force_ignore=True):
                    fork_valid(course, suffix=f" ({course.start_date} - {course.end_date})")
                else:
                    fork_invalid(course)

    cli = click.CommandCollection(sources=[naucse, elsa_group])

    return cli()


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
