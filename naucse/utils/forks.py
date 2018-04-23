from datetime import date, datetime, time
from typing import Any, Dict, Optional

from flask import url_for
from flask_frozen import UrlForLogger
from git import Repo

from naucse import views
from naucse.models import Course
from naucse.utils.views import page_content_cache_key, get_edit_info


def get_course_from_slug(slug: str) -> Course:
    """ Gets the actual course instance from a slug.
    """
    parts = slug.split("/")

    if parts[0] == "course":
        return views.model.courses[parts[1]]
    else:
        return views.model.runs[(int(parts[0]), parts[1])]


def course_info(slug: str, *args, **kwargs) -> Dict[str, Any]:
    """Return info about the given course.

    Return some extra info when it's a run (based on COURSE_INFO/RUN_INFO)
    """
    course = get_course_from_slug(slug)

    if course.is_link():
        raise ValueError("Circular dependency.")

    if "course" in slug:
        attributes = Course.COURSE_INFO
    else:
        attributes = Course.RUN_INFO

    data = {}

    for attr in attributes:
        val = getattr(course, attr)

        if isinstance(val, (date, datetime, time)):
            val = val.isoformat()

        data[attr] = val

    return data


def serialize_license(license) -> Optional[Dict[str, str]]:
    """Serialize a License instance into a dict.
    """
    if license:
        return {
            "url": license.url,
            "title": license.title
        }

    return None


def render(page_type: str, slug: str, *args, **kwargs) -> Dict[str, Any]:
    """Return a rendered page for a course, based on page_type and slug.
    """
    course = get_course_from_slug(slug)

    if course.is_link():
        raise ValueError("Circular dependency.")

    path = []
    if kwargs.get("request_url"):
        path = [kwargs["request_url"]]

    logger = UrlForLogger(views.app)
    with views.app.test_request_context(*path):
        with logger:

            info = {
                "course": {
                    "title": course.title,
                    "url": views.course_url(course),
                    "vars": course.vars,
                    "canonical": course.canonical,
                    "is_derived": course.is_derived,
                },
            }

            if page_type == "course":
                info["content"] = views.course_content(course)
                info["edit_info"] = get_edit_info(course.edit_path)

            elif page_type == "calendar":
                info["content"] = views.course_calendar_content(course)
                info["edit_info"] = get_edit_info(course.edit_path)

            elif page_type == "calendar_ics":
                info["calendar"] = str(views.generate_calendar_ics(course))
                info["edit_info"] = get_edit_info(course.edit_path)

            elif page_type == "course_page":
                lesson_slug, page, solution, *_ = args
                lesson = views.model.get_lesson(lesson_slug)

                content_offer_key = kwargs.get("content_key")

                not_processed = object()
                content = not_processed

                if content_offer_key is not None:
                    # the base repository has a cached version of the content
                    content_key = page_content_cache_key(Repo("."), lesson_slug, page, solution, course.vars)

                    # if the key matches what would be produced here, let's not return anything
                    # and the cached version will be used
                    if content_offer_key == content_key:
                        content = None

                request_url = kwargs.get("request_url")
                if request_url is None:
                    request_url = url_for('course_page', course=course, lesson=lesson, page=page, solution=solution)

                lesson_url, subpage_url, static_url = views.relative_url_functions(request_url, course, lesson)
                page, session, prv, nxt = views.get_page(course, lesson, page)

                # if content isn't cached or the version was refused, let's render
                # the content here (but just the content and not the whole page with headers, menus etc)
                if content is not_processed:
                    content = views.page_content(
                        lesson, page, solution, course,
                        lesson_url=lesson_url,
                        subpage_url=subpage_url,
                        static_url=static_url,
                        without_cache=True,
                    )

                if content is None:
                    info["content"] = None
                    info["content_urls"] = []
                else:
                    info["content"] = content["content"]
                    info["content_urls"] = content["urls"]

                info.update({
                    "page": {
                        "title": page.title,
                        "css": page.info.get("css"),  # not page.css since we want the css without limitation
                        "latex": page.latex,
                        "attributions": page.attributions,
                        "license": serialize_license(page.license),
                        "license_code": serialize_license(page.license_code)
                    },
                    "edit_info": get_edit_info(page.edit_path)
                })

                if session is not None:
                    info["session"] = {
                        "title": session.title,
                        "url": url_for("session_coverpage", course=course.slug, session=session.slug),
                        "slug": session.slug,
                    }

                prev_link, session_link, next_link = views.get_footer_links(course, session, prv, nxt, lesson_url)
                info["footer"] = {
                    "prev_link": prev_link,
                    "session_link": session_link,
                    "next_link": next_link
                }

            elif page_type == "session_coverpage":
                session_slug, coverpage, *_ = args

                session = course.sessions.get(session_slug)

                info.update({
                    "session": {
                        "title": session.title,
                        "url": url_for("session_coverpage", course=course.slug, session=session.slug),
                    },
                    "content": views.session_coverpage_content(course, session, coverpage),
                    "edit_info": get_edit_info(session.get_edit_path(course, coverpage)),
                })
            else:
                raise ValueError("Invalid page type.")

        # generate list of absolute urls which need to be frozen further
        urls = set()
        for endpoint, values in logger.iter_calls():
            url = url_for(endpoint, **values)
            if url.startswith(f"/{slug}"):  # this is checked once again in main repo, but let's save cache space
                urls.add(url)

        info["urls"] = list(urls)

    return info


def get_footer_links(slug, lesson_slug, page, request_url=None):
    course = get_course_from_slug(slug)

    if course.is_link():
        raise ValueError("Circular dependency.")

    try:
        lesson = views.model.get_lesson(lesson_slug)
    except LookupError:
        raise ValueError("Lesson not found")

    path = []
    if request_url is not None:
        path = [request_url]

    with views.app.test_request_context(*path):

        def lesson_url(lesson, *args, **kwargs):
            return url_for("course_page", course=course, lesson=lesson, *args, **kwargs)

        page, session, prv, nxt = views.get_page(course, lesson, page)
        prev_link, session_link, next_link = views.get_footer_links(course, session, prv, nxt, lesson_url)

    return {
        "prev_link": prev_link,
        "session_link": session_link,
        "next_link": next_link
    }
