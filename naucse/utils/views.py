import datetime
import hashlib
import json
import os
from collections import deque, defaultdict
from pathlib import Path

from arca.exceptions import PullError, BuildError, RequirementsMismatch
from arca.utils import get_hash_for_file

absolute_urls_to_freeze = deque()


def get_recent_runs(course):
    """Build a list of "recent" runs based on a course.

    By recent we mean: haven't ended yet, or ended up to ~2 months ago
    (Note: even if naucse is hosted dynamically,
    it's still beneficial to show recently ended runs.)
    """
    recent_runs = []
    if not course.start_date:
        today = datetime.date.today()
        cutoff = today - datetime.timedelta(days=2*30)
        this_year = today.year
        for year, run_year in reversed(course.root.run_years.items()):
            for run in run_year.runs.values():
                if not run.is_link() or (forks_enabled() and does_course_return_info(run, ["start_date", "end_date"])):
                    if run.base_course is course and run.end_date > cutoff:
                        recent_runs.append(run)

            if year < this_year:
                # Assume no run lasts for more than a year,
                # e.g. if it's Jan 2018, some run that started in 2017 may
                # be included, but don't even look through runs from 2016
                # or earlier.
                break
    recent_runs.sort(key=lambda r: r.start_date, reverse=True)
    return recent_runs


def list_months(start_date, end_date):
    """Return a span of months as a list of (year, month) tuples

    The months of start_date and end_date are both included.
    """
    months = []
    year = start_date.year
    month = start_date.month
    while (year, month) <= (end_date.year, end_date.month):
        months.append((year, month))
        month += 1
        if month > 12:
            month = 1
            year += 1
    return months


_naucse_tree_hash = {}


def get_naucse_tree_hash(repo):
    """ Returns the tree hash of the folder ``naucse``, which contains rendering mechanisms, in specified ``repo``.
    """
    from naucse.views import app
    global _naucse_tree_hash

    if _naucse_tree_hash.get(repo.git_dir):
        return _naucse_tree_hash[repo.git_dir]

    tree_hash = get_hash_for_file(repo, "naucse")

    if not app.config['DEBUG']:
        _naucse_tree_hash[repo.git_dir] = tree_hash

    return tree_hash


_lesson_tree_hash = defaultdict(dict)


def get_lesson_tree_hash(repo, lesson_slug):
    """ Returns the tree hash of the folder containing the lesson in specified ``repo``.
    """
    from naucse.views import app

    global _lesson_tree_hash

    if lesson_slug in _lesson_tree_hash[repo.git_dir]:
        return _lesson_tree_hash[repo.git_dir][lesson_slug]

    # ``repo.git_dir`` is path to the ``.git`` folder
    if not (Path(repo.git_dir).parent / "lessons" / lesson_slug).exists():
        raise FileNotFoundError

    commit = get_hash_for_file(repo, "lessons/" + lesson_slug)

    if not app.config['DEBUG']:
        _lesson_tree_hash[repo.git_dir][lesson_slug] = commit

    return commit


def forks_enabled():
    """ Returns if forks are enabled. By default they're not (for the purposes of local development).

    Forks can be enabled by setting FORKS_ENABLED environ variable to ``true``.
    """
    return os.environ.get("FORKS_ENABLED", "false") == "true"


def forks_raise_if_disabled():
    """ Raises ValueError if forks are not enabled.
    """
    if not forks_enabled():
        raise ValueError(
            "You must explicitly allow forks to be rendered.\n"
            "Set FORKS_ENABLED=true to enable them.")


def raise_errors_from_forks():
    """ Returns if errors from forks should be raised or handled in the default way.

    Only raising when a RAISE_FORK_ERRORS environ variable is set to ``true``.

    Default handling:

    * Not even basic course info is returned -> Left out of the list of courses
    * Error rendering a page
        * Lesson - if the lesson is canonical, canonical version is rendered with a warning
        * Everything else - templates/error_in_fork.html is rendered
    """
    return os.environ.get("RAISE_FORK_ERRORS", "false") == "true"


def does_course_return_info(course, extra_required=(), *, force_ignore=False):
    """ Returns if the the external course can be pulled and that it returns basic info about the course.

    Raises exception if :func:`raise_errors_from_forks` returns it should. (But not if ``force_ignore`` is set.)
    """
    from naucse.views import logger

    required = ["title", "description"] + list(extra_required)
    try:
        if isinstance(course.info, dict) and all([x in course.info for x in required]):
            return True

        if raise_errors_from_forks() and not force_ignore:
            raise ValueError(f"Couldn't get basic info about the course {course.slug}, "
                             f"the repo didn't return a dict or the required info is missing.")
        else:
            logger.error("There was an problem getting basic info out of forked course %s. "
                         "Suppressing, because this is the production branch.", course.slug)
    except (PullError, BuildError, RequirementsMismatch) as e:
        if raise_errors_from_forks() and not force_ignore:
            raise
        if isinstance(e, PullError):
            logger.error("There was an problem either pulling or cloning the forked course %s. "
                         "Suppressing, because this is the production branch.", course.slug)
        elif isinstance(e, RequirementsMismatch):
            logger.error("There are some extra requirements in the forked course %s. "
                         "Suppressing, because this is the production branch.", course.slug)
        else:
            logger.error("There was an problem getting basic info out of forked course %s. "
                         "Suppressing, because this is the production branch.", course.slug)
        logger.exception(e)

    return False


def page_content_cache_key(repo, lesson_slug, page, solution, course_vars=None) -> str:
    """ Returns a key under which content fragments will be stored in cache, depending on the page
        and the last commit which modified lesson rendering in ``repo``
    """
    return "commit:{}:content:{}".format(
        get_naucse_tree_hash(repo),
        hashlib.sha1(json.dumps(
            {
                "lesson": lesson_slug,
                "page": page,
                "solution": solution,
                "vars": course_vars,
                "lesson_tree_hash": get_lesson_tree_hash(repo, lesson_slug),
            },
            sort_keys=True
        ).encode("utf-8")).hexdigest()
    )


def edit_link(path):
    from naucse.views import model

    if path == Path("."):
        return f"https://github.com/{model.meta.slug}"

    return f"https://github.com/{model.meta.slug}/blob/{model.meta.branch}/{str(path)}"


def get_edit_icon():
    """ Should return None or some other icon from `templates/_bytesize_icons.html` if the fork is not on GitHub.
    """
    return "github"


def get_edit_page_name():
    """ Should return the name of the page where editing is possible, in Czech in the 6th case.
        Will be used to replace X in the sentence: `Uprav tuto stránku na X.`
    """
    return "GitHubu"


def get_edit_info(edit_path):
    return {
        "icon": get_edit_icon(),
        "page_name": get_edit_page_name(),
        "url": edit_link(edit_path)
    }
