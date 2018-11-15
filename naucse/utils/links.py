"""Functions for validation and further processing of metadata from forks.
"""
from xml.dom import SyntaxErr

from naucse.models import Page
from naucse.sanitize import DisallowedStyle


class InvalidInfo(Exception):
    pass


def process_info_about_object(info, required_fields=(), *, set_default=(), allow_none=False, check_str=False):
    if info is None:
        if allow_none:
            return None
        raise InvalidInfo("Information about an object from fork is required.")

    if not isinstance(info, dict):
        raise InvalidInfo("Information about an object from fork is in the wrong format (must be a dict)")

    for field in required_fields:
        if field not in info or (check_str and not isinstance(info[field], str)):
            raise InvalidInfo("Required information is missing from info about an object from fork")

    for field in set_default:
        info.setdefault(field, None)

    return info


def process_course_data(course, slug=None):
    course = process_info_about_object(course, ["title", "url"])

    course["slug"] = slug
    course.setdefault("vars", {})

    if not isinstance(course["vars"], dict):
        raise InvalidInfo("Course vars are invalid")

    course.setdefault("canonical", False)
    course.setdefault("is_derived", False)

    return course


def process_session_data(session, slug=None):
    session = process_info_about_object(session, ["title", "url"], allow_none=True)

    if slug is not None:
        session["slug"] = slug

    return session


def process_license_data(license):
    return process_info_about_object(license, ["title", "url"], allow_none=True)


def process_page_data(page):
    # set the keys to None, otherwise the template will throw a key error
    page = process_info_about_object(page, set_default=["title", "latex", "attributions"])

    page["license"] = process_license_data(page.get("license"))
    page["license_code"] = process_license_data(page.get("license_code"))

    page.setdefault("css", None)

    if page["css"]:
        try:
            Page.limit_css_to_lesson_content(page["css"])
        except SyntaxErr:
            raise DisallowedStyle(DisallowedStyle.COULD_NOT_PARSE)

    return page


def process_edit_info(edit_info_data):
    return process_info_about_object(edit_info_data, ["url", "icon", "page_name"], allow_none=True, check_str=True)


def process_footer_link(link):
    try:
        return process_info_about_object(link, ["title", "url"], allow_none=True, check_str=True)
    except InvalidInfo:
        return None


def process_footer_data(footer):
    if footer is None or not isinstance(footer, dict):
        return None, None, None

    to_return = []

    for link_type in "prev_link", "session_link", "next_link":
        link = footer.get(link_type)

        to_return.append(process_footer_link(link))

    return to_return
