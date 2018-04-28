import calendar
import datetime
import logging
import os
from urllib.parse import urljoin
from pathlib import Path

import ics
from arca.exceptions import PullError, BuildError, RequirementsMismatch
from arca.utils import is_dirty
from flask import Flask, render_template, url_for, send_from_directory, request, redirect
from flask import abort, Response
from git import Repo
from jinja2 import StrictUndefined
from jinja2.exceptions import TemplateNotFound
from werkzeug.local import LocalProxy

from naucse import models
from naucse.freezer import temporary_url_for_logger
from naucse.models import allowed_elements_parser
from naucse.templates import setup_jinja_env, vars_functions
from naucse.urlconverters import register_url_converters
from naucse.utils import links
from naucse.utils.links import (process_course_data, process_session_data, process_page_data, process_footer_data,
                                InvalidInfo)
from naucse.utils.models import arca
from naucse.utils.views import get_recent_runs, list_months
from naucse.utils.views import does_course_return_info
from naucse.utils.views import absolute_urls_to_freeze, raise_errors_from_forks
from naucse.utils.views import page_content_cache_key, get_edit_info
from naucse.validation import DisallowedStyle, DisallowedElement, InvalidHTML

# so it can be mocked
import naucse.utils.views

app = Flask('naucse')
app.config['TEMPLATES_AUTO_RELOAD'] = True
logger = logging.getLogger("naucse")
logger.setLevel(logging.DEBUG)

setup_jinja_env(app.jinja_env)
POSSIBLE_FORK_EXCEPTIONS = (PullError, BuildError, DisallowedStyle, DisallowedElement, FileNotFoundError,
                            RequirementsMismatch, InvalidHTML, InvalidInfo)

_cached_model = None


@LocalProxy
def model():
    """Return the root of the naucse model

    In debug mode (elsa serve), a new model is returned for each requests,
    so changes are picked up.

    In non-debug mode (elsa freeze), a single model is used (and stored in
    _cached_model), so that metadata is only read once.
    """
    global _cached_model
    if _cached_model:
        return _cached_model
    model = models.Root(os.path.join(app.root_path, '..'))
    if not app.config['DEBUG']:
        _cached_model = model
    return model


register_url_converters(app, model)

app.jinja_env.undefined = StrictUndefined


def template_function(func):
    app.jinja_env.globals[func.__name__] = func
    return func


@template_function
def static(filename):
    return url_for('static', filename=filename)


@template_function
def course_url(course):
    return url_for('course', course=course)


@template_function
def lesson_url(lesson, page='index', solution=None):
    return url_for('lesson', lesson=lesson, page=page, solution=solution)


@template_function
def session_url(course, session, coverpage='front'):
    return url_for("session_coverpage",
                   course=course,
                   session=session,
                   coverpage=coverpage)


@app.route('/')
def index():
    return render_template("index.html",
                           edit_info=get_edit_info(Path(".")))


@app.route('/runs/')
@app.route('/<int:year>/')
@app.route('/runs/<any(all):all>/')
def runs(year=None, all=None):
    today = datetime.date.today()

    # List of years to show in the pagination
    # If the current year is not there (no runs that start in the current year
    # yet), add it manually
    all_years = model.safe_run_years.keys()
    if today.year not in all_years:
        all_years.append(today.year)
    first_year, last_year = min(all_years), max(all_years)

    if year is not None:
        if year > last_year:
            # Instead of showing a future year, redirect to the 'Current' page
            return redirect(url_for('runs'))
        if year not in all_years:
            # Otherwise, if there are no runs in requested year, return 404.
            abort(404)

    if all is not None:
        run_data = model.safe_run_years

        paginate_prev = {'year': first_year}
        paginate_next = {'all': 'all'}
    elif year is None:
        # Show runs that are either ongoing or ended in the last 3 months
        runs = (model.runs_from_year(today.year) +
                model.runs_from_year(today.year - 1) +
                model.runs_from_year(today.year - 2))
        ongoing = [run for run in runs if run.end_date >= today]
        cutoff = today - datetime.timedelta(days=3*31)
        recent = [run for run in runs if today > run.end_date > cutoff]
        run_data = {"ongoing": ongoing, "recent": recent}

        paginate_prev = {'year': None}
        paginate_next = {'year': last_year}
    else:
        run_data = {year: [run for run
                           in model.runs_from_year(year) +
                              model.runs_from_year(year - 1)
                           if run.end_date.year >= year]}

        past_years = [y for y in all_years if y < year]
        if past_years:
            paginate_next = {'year': max(past_years)}
        else:
            paginate_next = {'all': 'all'}

        future_years = [y for y in all_years if y > year]
        if future_years:
            paginate_prev = {'year': min(future_years)}
        else:
            paginate_prev = {'year': None}

    return render_template("run_list.html",
                           run_data=run_data,
                           title="Seznam offline kurzů Pythonu",
                           today=datetime.date.today(),
                           year=year,
                           all=all,
                           all_years=all_years,
                           paginate_next=paginate_next,
                           paginate_prev=paginate_prev,
                           edit_info=get_edit_info(model.runs_edit_path))


@app.route('/courses/')
def courses():
    # since even the basic info about the forked courses can be broken,
    # we need to make sure the required info is provided.
    # If ``RAISE_FORK_ERRORS`` is set, exceptions are raised here,
    # otherwise the course is ignored completely.
    safe_courses = []

    for course in model.courses.values():
        if not course.is_link():
            if not course.is_meta:
                safe_courses.append(course)
        elif naucse.utils.views.forks_enabled() and does_course_return_info(course):
            safe_courses.append(course)

    return render_template("course_list.html",
                           courses=safe_courses,
                           title="Seznam online kurzů Pythonu",
                           edit_info=get_edit_info(model.courses_edit_path))


@app.route('/lessons/<lesson_slug:lesson>/static/<path:path>', defaults={"course": None})
@app.route('/<course:course>/<lesson_slug:lesson>/static/<path:path>')
def lesson_static(course, lesson, path):
    """Get the endpoint for static files in lessons.

    Args:
        course  optional info about which course the static file is for
        lesson  lesson in which is the file located
        path    path to file in the static folder

    Returns:
        endpoint for the static file
    """
    lesson_slug = lesson
    try:
        lesson = model.get_lesson(lesson_slug)
    except LookupError:
        lesson = None

    if course is not None and course.is_link():  # is static file from a link?
        naucse.utils.views.forks_raise_if_disabled()

        try:
            return send_from_directory(*course.lesson_static(lesson_slug, path))
        except (PullError, FileNotFoundError):
            # the file cannot be retrieved, try to use canonical file instead
            pass

    # continue only if the lesson is canonical
    if lesson is None:
        abort(404)

    directory = str(lesson.path)
    filename = os.path.join('static', path)
    return send_from_directory(directory, filename)


def lesson_static_generator_dir(lesson_slug, static_dir, search_dir):
    """Generate all lesson_static calls from director ``search_dir``.

    Yields paths relative to ``static_dir`` for lesson with
    the slug ``lesson_slug``.
    """
    if not search_dir.exists():
        return

    for static_file in search_dir.iterdir():

        if static_file.is_dir():
            yield from lesson_static_generator_dir(lesson_slug, static_dir, static_file)
            continue

        relative = static_file.relative_to(static_dir)

        yield ("lesson_static", {"lesson": lesson_slug, "path": str(relative)})


def lesson_static_generator():
    """Generate all static URLs

    When freezing naucse and nothing has been changed, almost everything
    comes out of cache, and the URLs are not registered via ``url_for``
    but instead are registered as absolute urls.
    Frozen-Flask however doesn't register the endpoints as visited when
    freezing absolute URLs, and the following error is thrown:

    ```
    flask_frozen.MissingURLGeneratorWarning: Nothing frozen for endpoints lesson_static. Did you forget a URL generator?
    ```

    This generator shuts it up, generating all the urls for canonical
    lesson_static, including subdirectories.
    """
    for collection in model.collections.values():
        for lesson in collection.lessons.values():
            static = Path(lesson.path / "static").resolve()

            if not static.exists():
                continue

            yield from lesson_static_generator_dir(lesson.slug, static, static)


def course_content(course):
    def lesson_url(lesson, *args, **kwargs):
        if kwargs.get("page") == "index":
            kwargs.pop("page")

        return url_for('course_page', course=course, lesson=lesson, *args, **kwargs)

    return render_template(
        "content/course.html",
        course=course,
        title=course.title,
        plan=course.sessions,
        lesson_url=lesson_url,
        **vars_functions(course.vars)
    )


@app.route('/<course:course>/')
def course(course):
    if course.is_link():
        naucse.utils.views.forks_raise_if_disabled()

        try:
            data_from_fork = course.render_course(request_url=request.path)
        except POSSIBLE_FORK_EXCEPTIONS as e:
            if raise_errors_from_forks():
                raise

            # there's no way to replace this page, render an error page instead
            logger.error("There was an error rendering url %s for course '%s'", request.path, course.slug)
            logger.exception(e)
            return render_template(
                "error_in_fork.html",
                malfunctioning_course=course,
                edit_info=get_edit_info(course.edit_path),
                faulty_page="course",
                root_slug=model.meta.slug,
                travis_build_id=os.environ.get("TRAVIS_BUILD_ID"),
            )
        kwargs = {
            "course_content": data_from_fork.get("content"),
            "edit_info": links.process_edit_info(data_from_fork.get("edit_info")),
        }
    else:
        content = course_content(course)
        allowed_elements_parser.reset_and_feed(content)

        kwargs = {
            "course_content": content,
            "edit_info": get_edit_info(course.edit_path),
        }

    recent_runs = get_recent_runs(course)

    try:
        return render_template(
            "course.html",
            course=course,
            title=course.title,
            recent_runs=recent_runs,
            **kwargs
        )
    except TemplateNotFound:
        abort(404)


def get_page(course, lesson, page):
    for session in course.sessions.values():
        for material in session.materials:
            if (material.type == "page" and material.page.lesson.slug == lesson.slug):
                material = material.subpages[page]
                page = material.page
                nxt = material.next
                prv = material.prev
                break
        else:
            continue
        break
    else:
        page = lesson.pages[page]
        session = None
        prv = nxt = None

    return page, session, prv, nxt


def get_footer_links(course, session, prv, nxt, lesson_url):
    """Return info about prev/next page based on current session, page, etc.
    """
    prev_link = None
    if prv is not None:
        prev_link = {
            "url": lesson_url(prv.page.lesson, page=prv.page.slug),
            "title": prv.page.title,
        }

    session_link = None
    if session is not None:
        session_link = {
            "url": session_url(course.slug, session.slug),
            "title": session.title,
        }

    next_link = None
    if nxt is not None:
        next_link = {
            "url": lesson_url(nxt.page.lesson, page=nxt.page.slug),
            "title": nxt.page.title,
        }
    elif session is not None:
        next_link = {
            "url": session_url(course.slug, session.slug, coverpage="back"),
            "title": "Závěr lekce",
        }

    return prev_link, session_link, next_link


def get_relative_url(current, target):
    """Return an URL to ``target`` relative to ``current``.
    """
    rel = os.path.relpath(target, current)

    if rel[-1] != "/":
        if "." not in rel.split("/")[-1]:
            rel += "/"

    if not rel.startswith("../") and rel != "./":
        rel = f"./{rel}"

    return rel


def relative_url_functions(current_url, course, lesson):
    """Return relative URL generators based on current page.
    """
    def lesson_url(lesson, *args, **kwargs):
        if not isinstance(lesson, str):
            lesson = lesson.slug

        if course is not None:
            absolute = url_for('course_page', course=course, lesson=lesson, *args, **kwargs)
        else:
            absolute = url_for('lesson', lesson=lesson, *args, **kwargs)
        return get_relative_url(current_url, absolute)

    def subpage_url(page_slug):
        if course is not None:
            absolute = url_for('course_page', course=course, lesson=lesson, page=page_slug)
        else:
            absolute = url_for('lesson', lesson=lesson, page=page_slug)

        return get_relative_url(current_url, absolute)

    def static_url(path):
        absolute = url_for('lesson_static', lesson=lesson, path=path, course=course)

        return get_relative_url(current_url, absolute)

    return lesson_url, subpage_url, static_url


def page_content(lesson, page, solution=None, course=None, lesson_url=None, subpage_url=None, static_url=None,
                 without_cache=False):
    variables = None
    if course is not None:
        variables = course.vars

    def content_creator():
        """Return the content and all relative URLs used in it.

        Since the content is stored in cache and can be reused elsewhere, URLs
        must be stored as relative to the current page, so new absolute urls
        can be generated where the content is reused.
        """
        with temporary_url_for_logger(app) as logger:
            with logger:
                content = page.render_html(
                    solution=solution,
                    static_url=static_url,
                    lesson_url=lesson_url,
                    subpage_url=subpage_url,
                    vars=variables
                )

            absolute_urls = [url_for(logged[0], **logged[1]) for logged in logger.logged_calls]

        relative_urls = [get_relative_url(request.path, x) for x in absolute_urls]

        return {"content": content, "urls": relative_urls}

    # Only use the cache if there are no local changes
    # and not rendering in fork
    if without_cache or is_dirty(Repo(".")):
        return content_creator()

    # Since ARCA_IGNORE_CACHE_ERRORS is used, this won't fail in forks
    # even if the cache doesn't work.
    # This is only dangerous if the fork sets absolute path to cache and
    # CurrentEnvironmentBackend or VenvBackend are used locally.
    # FIXME? But I don't think there's a way to prevent writing
    # to a file in those backends
    content_key = page_content_cache_key(Repo("."), lesson.slug, page.slug, solution, variables)
    cached = arca.region.get_or_create(content_key, content_creator)

    # The urls are added twice to ``absolute_urls_to_freeze``
    # when the content is created.
    # But it doesn't matter, duplicate URLs are skipped.
    absolute_urls = [urljoin(request.path, x) for x in cached["urls"]]
    absolute_urls_to_freeze.extend(absolute_urls)

    return cached


@app.route('/<course:course>/<lesson_slug:lesson>/', defaults={'page': 'index'})
@app.route('/<course:course>/<lesson_slug:lesson>/<page>/')
@app.route('/<course:course>/<lesson_slug:lesson>/<page>/solutions/<int:solution>/')
def course_page(course, lesson, page, solution=None):
    lesson_slug = lesson
    page_slug = page

    try:
        lesson = model.get_lesson(lesson_slug)
        canonical_url = url_for('lesson', lesson=lesson, _external=True)
    except LookupError:
        lesson = canonical_url = None

    kwargs = {}
    prev_link = session_link = next_link = session = None

    if course.is_link():
        naucse.utils.views.forks_raise_if_disabled()

        fork_kwargs = {"request_url": request.path}

        try:
            # Checks if the rendered page content is in cache locally
            # to offer it to the fork.
            # ``course.vars`` calls ``course_info`` so it has to be in
            # the try block.
            # The function can also raise FileNotFoundError if the
            # lesson doesn't exist in repo.
            content_key = page_content_cache_key(arca.get_repo(course.repo, course.branch),
                                                 lesson_slug, page, solution, course.vars)
            content_offer = arca.region.get(content_key)

            # We've got the fragment in cache, let's offer it to the fork.
            if content_offer:
                fork_kwargs["content_key"] = content_key

            data_from_fork = course.render_page(lesson_slug, page, solution, **fork_kwargs)

            content = data_from_fork["content"]

            if content is None:
                # the offer was accepted
                content = content_offer["content"]
                absolute_urls_to_freeze.extend([urljoin(request.path, x)
                                                for x in content_offer["urls"]])
            else:
                # the offer was rejected or the the fragment was not in cache
                arca.region.set(content_key, {"content": content, "urls": data_from_fork["content_urls"]})
                absolute_urls_to_freeze.extend([urljoin(request.path, x)
                                                for x in data_from_fork["content_urls"]])

            # compatibility
            page = process_page_data(data_from_fork.get("page"))
            course = process_course_data(data_from_fork.get("course"), slug=course.slug)
            session = process_session_data(data_from_fork.get("session"))
            kwargs["edit_info"] = links.process_edit_info(data_from_fork.get("edit_info"))
            prev_link, session_link, next_link = process_footer_data(data_from_fork.get("footer"))

            title = '{}: {}'.format(course["title"], page["title"])
        except POSSIBLE_FORK_EXCEPTIONS as e:
            if raise_errors_from_forks():
                raise

            rendered_replacement = False

            logger.error("There was an error rendering url %s for course '%s'", request.path, course.slug)
            if lesson is not None:
                try:
                    logger.error("Rendering the canonical version with a warning.")

                    lesson_url, subpage_url, static_url = relative_url_functions(request.path, course, lesson)
                    page = lesson.pages[page]
                    content = page_content(
                        lesson, page, solution, course,
                        lesson_url=lesson_url, subpage_url=subpage_url, static_url=static_url
                    )["content"]
                    title = '{}: {}'.format(course.title, page.title)

                    try:
                        prev_link, session_link, next_link = course.get_footer_links(lesson.slug, page_slug,
                                                                                     request_url=request.path)
                    except POSSIBLE_FORK_EXCEPTIONS as e:
                        if raise_errors_from_forks():
                            raise

                        # The fork is failing spectacularly, so the footer
                        # links aren't that important
                        logger.error("Could not retrieve even footer links from the fork at page %s", request.path)
                        logger.exception(e)

                    rendered_replacement = True
                    kwargs["edit_info"] = get_edit_info(page.edit_path)
                    kwargs["error_in_fork"] = True
                    kwargs["travis_build_id"] = os.environ.get("TRAVIS_BUILD_ID")

                except Exception as canonical_error:
                    logger.error("Rendering the canonical version failed.")
                    logger.exception(canonical_error)

            if not rendered_replacement:
                logger.exception(e)
                return render_template(
                    "error_in_fork.html",
                    malfunctioning_course=course,
                    edit_info=get_edit_info(course.edit_path),
                    faulty_page="lesson",
                    lesson=lesson_slug,
                    pg=page_slug,  # avoid name conflict
                    solution=solution,
                    root_slug=model.meta.slug,
                    travis_build_id=os.environ.get("TRAVIS_BUILD_ID"),
                )
    else:
        if lesson is None:
            abort(404)

        lesson_url, subpage_url, static_url = relative_url_functions(request.path, course, lesson)
        page, session, prv, nxt = get_page(course, lesson, page)
        prev_link, session_link, next_link = get_footer_links(course, session, prv, nxt, lesson_url)

        content = page_content(
            lesson, page, solution, course=course, lesson_url=lesson_url, subpage_url=subpage_url, static_url=static_url
        )
        content = content["content"]
        allowed_elements_parser.reset_and_feed(content)
        title = '{}: {}'.format(course.title, page.title)

        kwargs["edit_info"] = get_edit_info(page.edit_path)

    if solution is not None:
        kwargs["solution_number"] = int(solution)

    return render_template(
        "lesson.html",
        canonical_url=canonical_url,
        title=title,
        content=content,
        prev_link=prev_link,
        session_link=session_link,
        next_link=next_link,
        root_slug=model.meta.slug,
        course=course,
        lesson=lesson,
        page=page,
        solution=solution,
        session=session,
        **kwargs
    )


@app.route('/lessons/<lesson:lesson>/', defaults={'page': 'index'})
@app.route('/lessons/<lesson:lesson>/<page>/')
@app.route('/lessons/<lesson:lesson>/<page>/solutions/<int:solution>/')
def lesson(lesson, page, solution=None):
    """Render the html of the given lesson page."""

    lesson_url, subpage_url, static_url = relative_url_functions(request.path, None, lesson)

    page = lesson.pages[page]

    content = page_content(lesson, page, solution=solution, lesson_url=lesson_url,
                           subpage_url=subpage_url,
                           static_url=static_url)

    content = content["content"]
    allowed_elements_parser.reset_and_feed(content)

    kwargs = {}
    if solution is not None:
        kwargs["solution_number"] = int(solution)

    return render_template(
        "lesson.html",
        content=content,
        page=page,
        lesson=lesson,
        edit_info=get_edit_info(page.edit_path),
        title=page.title,
        **kwargs
    )


def session_coverpage_content(course, session, coverpage):
    def lesson_url(lesson, *args, **kwargs):
        if kwargs.get("page") == "index":
            kwargs.pop("page")

        return url_for('course_page', course=course, lesson=lesson, *args, **kwargs)

    content = session.get_coverpage_content(course, coverpage, app)

    homework_section = False
    link_section = False
    cheatsheet_section = False
    for mat in session.materials:
        if mat.url_type == "homework":
            homework_section = True
        if mat.url_type == "link":
            link_section = True
        if mat.url_type == "cheatsheet":
            cheatsheet_section = True

    return render_template(
        "content/coverpage.html" if coverpage == "front" else "content/backpage.html",
        course=course,
        session=session,
        homework_section=homework_section,
        link_section=link_section,
        cheatsheet_section=cheatsheet_section,
        content=content,
        lesson_url=lesson_url,
        **vars_functions(course.vars),
    )


@app.route('/<course:course>/sessions/<session>/', defaults={'coverpage': 'front'})
@app.route('/<course:course>/sessions/<session>/<coverpage>/')
def session_coverpage(course, session, coverpage):
    """Render the session coverpage.

    Args:
        course      course where the session belongs
        session     name of the session
        coverpage   coverpage of the session, front is default

    Returns:
        rendered session coverpage
    """
    if course.is_link():
        naucse.utils.views.forks_raise_if_disabled()

        try:
            data_from_fork = course.render_session_coverpage(session, coverpage, request_url=request.path)

            kwargs = {
                "course": process_course_data(data_from_fork.get("course"), slug=course.slug),
                "session": process_session_data(data_from_fork.get("session"), slug=session),
                "edit_info": links.process_edit_info(data_from_fork.get("edit_info")),
                "content": data_from_fork["content"]
            }
        except POSSIBLE_FORK_EXCEPTIONS as e:
            if raise_errors_from_forks():
                raise

            # there's no way to replace this page, render an error page instead
            logger.error("There was an error rendering url %s for course '%s'", request.path, course.slug)
            logger.exception(e)
            return render_template(
                "error_in_fork.html",
                malfunctioning_course=course,
                edit_info=get_edit_info(course.edit_path),
                faulty_page=f"session_{coverpage}",
                session=session,
                root_slug=model.meta.slug,
                travis_build_id=os.environ.get("TRAVIS_BUILD_ID"),
            )
    else:
        session = course.sessions.get(session)

        content = session_coverpage_content(course, session, coverpage)
        allowed_elements_parser.reset_and_feed(content)

        kwargs = {
            "course": course,
            "session": session,
            "edit_info": get_edit_info(session.get_edit_path(course, coverpage)),
            "content": content
        }

    return render_template("coverpage.html", **kwargs)


def course_calendar_content(course):
    sessions_by_date = {s.date: s for s in course.sessions.values()}

    return render_template(
        'content/course_calendar.html',
        course=course,
        sessions_by_date=sessions_by_date,
        months=list_months(course.start_date,
                           course.end_date),
        calendar=calendar.Calendar()
    )


@app.route('/<course:course>/calendar/')
def course_calendar(course):
    if course.is_link():
        naucse.utils.views.forks_raise_if_disabled()

        try:
            data_from_fork = course.render_calendar(request_url=request.path)

            course = process_course_data(data_from_fork.get("course"), slug=course.slug)
            edit_info = links.process_edit_info(data_from_fork.get("edit_info"))
        except POSSIBLE_FORK_EXCEPTIONS as e:
            if raise_errors_from_forks():
                raise

            logger.error("There was an error rendering url %s for course '%s'", request.path, course.slug)
            logger.exception(e)
            return render_template(
                "error_in_fork.html",
                malfunctioning_course=course,
                edit_info=get_edit_info(course.edit_path),
                faulty_page="calendar",
                root_slug=model.meta.slug,
                travis_build_id=os.environ.get("TRAVIS_BUILD_ID"),
            )

        kwargs = {
            "course": course,
            "edit_info": edit_info,
            "content": data_from_fork.get("content")
        }
    else:
        if not course.start_date:
            abort(404)

        content = course_calendar_content(course)
        allowed_elements_parser.reset_and_feed(content)

        kwargs = {
            "course": course,
            "edit_info": get_edit_info(course.edit_path),
            "content": content
        }

    return render_template('course_calendar.html', **kwargs)


def generate_calendar_ics(course):
    calendar = ics.Calendar()
    for session in course.sessions.values():
        if session.start_time:
            start_time = session.start_time
            end_time = session.end_time
        else:
            raise ValueError("One of the sessions doesn't have a start time.")

        cal_event = ics.Event(
            name=session.title,
            begin=start_time,
            end=end_time,
            uid=url_for("session_coverpage",
                        course=course,
                        session=session.slug,
                        _external=True),
        )
        calendar.events.append(cal_event)

    return calendar


@app.route('/<course:course>/calendar.ics')
def course_calendar_ics(course):
    if not course.start_date:
        abort(404)

    if course.is_link():
        naucse.utils.views.forks_raise_if_disabled()

        try:
            data_from_fork = course.render_calendar_ics(request_url=request.path)
        except POSSIBLE_FORK_EXCEPTIONS as e:
            if raise_errors_from_forks():
                raise

            logger.error("There was an error rendering url %s for course '%s'", request.path, course.slug)
            logger.exception(e)
            return render_template(
                "error_in_fork.html",
                malfunctioning_course=course,
                edit_info=get_edit_info(course.edit_path),
                faulty_page="calendar",
                root_slug=model.meta.slug,
                travis_build_id=os.environ.get("TRAVIS_BUILD_ID"),
            )

        calendar = data_from_fork["calendar"]
    else:
        try:
            calendar = generate_calendar_ics(course)
        except ValueError:
            abort(404)

    return Response(str(calendar), mimetype="text/calendar")
