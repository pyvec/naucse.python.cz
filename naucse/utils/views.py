import datetime
import hashlib
import json
import os
from collections import deque, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from xml.dom import SyntaxErr

import cssutils
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


class DisallowedElement(Exception):
    pass


class InvalidHTML(DisallowedElement):
    pass


class DisallowedAttribute(DisallowedElement):
    pass


class DisallowedStyle(Exception):

    _BASE = "Style element or page css are only allowed when they modify .dataframe elements."
    COULD_NOT_PARSE = _BASE + " Ccould not parse the styles and verify."
    OUT_OF_SCOPE = _BASE + " Rendered page contains a style that modifies something else."


class AllowedElementsParser(HTMLParser):
    """
    This parser is used on all HTML returned from forked repositories.

    It raises exceptions in two cases:

    * :class:`DisallowedElement` - if a element not defined in :attr:`allowed_elements` is used
    * :class:`DisallowedStyle` - if a <style> element contains unparsable css or if it modifies something
      different than ``.dataframe`` elements.
    """

    def __init__(self, **kwargs):
        super(AllowedElementsParser, self).__init__(**kwargs)
        self.css_parser = cssutils.CSSParser(raiseExceptions=True)

        #: Set of allowed HTML elements
        #: It has been compiled out of elements currently used in canonical lessons
        self.allowed_elements = {
            # functional:
            'a', 'abbr', 'audio', 'img', 'source',

            # styling:
            'big', 'blockquote', 'code', 'font', 'i', 'tt', 'kbd', 'u', 'var', 'small', 'em', 'strong', 'sub',

            # formatting:
            'br', 'div', 'hr', 'p', 'pre', 'span',

            # lists:
            'dd', 'dl', 'dt', 'li', 'ul', 'ol',

            # headers:
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',

            # tables:
            'table', 'tbody', 'td', 'th', 'thead', 'tr',

            # icons:
            'svg', 'circle', 'path',

            # A special check is applied in :meth:`handle_data` method
            # (only ``.dataframe`` styles allowed, generated from notebook converter)
            'style',
        }

        #: Set of allowed HTML attributes
        #: Compiled out of currently used in canonical lesson
        self.allowed_attributes = {
            'alt', 'aria-hidden', 'border', 'class', 'color', 'colspan', 'controls', 'cx', 'cy', 'd', 'halign', 'href',
            'id', 'r', 'rowspan', 'src', 'start', 'title', 'type', 'valign', 'viewbox',

            # inline styles generated from notebook converter
            'style',
        }

        self.attrs = set()

    def error(self, message):
        raise InvalidHTML(message)

    def check_attributes(self, attrs):
        attr_names = set([x[0] for x in attrs])

        if len(attr_names - self.allowed_attributes):
            raise DisallowedAttribute("Attributes '{}' are not allowed".format(", ".join(attr_names)))

    def handle_starttag(self, tag, attrs):
        if tag not in self.allowed_elements:
            raise DisallowedElement(f"Element {tag} is not allowed.")

        self.check_attributes(attrs)

    def handle_startendtag(self, tag, attrs):
        if tag not in self.allowed_elements:
            raise DisallowedElement(f"Element {tag} is not allowed.")

        self.check_attributes(attrs)

    def handle_data(self, data):
        if self.lasttag == "style":
            self.validate_css(data)

    def reset_and_feed(self, data):
        self.reset()
        self.feed(data)

    def allow_selector(self, selector: str):
        if not selector.startswith(".dataframe "):
            return False

        return True

    def validate_css(self, data):
        try:
            parsed_css = self.css_parser.parseString(data)
        except SyntaxErr:
            raise DisallowedStyle(DisallowedStyle.COULD_NOT_PARSE)
        else:
            if len(parsed_css.cssRules) == 0:
                return

            if not all([self.allow_selector(selector.selectorText)
                        for rule in parsed_css.cssRules
                        for selector in rule.selectorList]):
                raise DisallowedStyle(DisallowedStyle.OUT_OF_SCOPE)


def forks_enabled():
    """ Returns if forks are enabled. By default they're not (for the purposes of local development).

    Forks can be enabled by setting FORKS_ENABLED environ variable to ``true``.
    """
    return os.environ.get("FORKS_ENABLED", "false") == "true"


def forks_raise_if_disabled():
    """ Raises ValueError if forks are not enabled.
    """
    if not forks_enabled():
        raise ValueError("You must explicitly allow forks to be rendered.")


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
