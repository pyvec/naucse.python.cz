from pathlib import Path

import pytest

from naucse import models
from naucse.edit_info import get_local_repo_info

from test_naucse.conftest import assert_yaml_dump, add_test_course

class DummyRenderer:
    """Renderer that returns lessons from a dict

    Mocks the get_lessons method of naucse_render or arca_renderer.Renderer.
    """

    def __init__(self, course=None, lessons=None):
        self.course = course
        self._lessons = lessons or {}

    def get_course(self, slug, *, version, path):
        return self.course

    def get_lessons(self, lessons, *, vars, path):
        return {slug: self._lessons[slug] for slug in lessons}


@pytest.fixture
def empty_course(model):
    add_test_course(model, 'courses/minimal', {
        'title': 'A minimal course',
        'sessions': [],
    })
    return model.courses['courses/minimal']


def check_empty_course_attrs(empty_course, *, source_file=None):
    assert empty_course.slug == 'courses/minimal'
    assert empty_course.parent == empty_course.root
    assert empty_course.title == 'A minimal course'
    assert empty_course.subtitle == None
    assert empty_course.description == None
    assert empty_course.long_description == ''
    assert empty_course.vars == {}
    assert empty_course.place == None
    assert empty_course.time_description == None
    assert empty_course.default_time == None
    assert empty_course.sessions == {}
    assert empty_course.source_file == source_file
    assert empty_course.start_date == None
    assert empty_course.end_date == None
    assert empty_course.derives == None
    assert empty_course.base_course == None
    assert empty_course.get_recent_derived_runs() == []


def test_empty_course_attrs(model, empty_course):
    assert empty_course.root == model
    check_empty_course_attrs(empty_course)


def test_get_lesson_url(empty_course):
    """Generating lessons URLs doesn't need the lesson to be available"""
    assert empty_course.get_lesson_url('any/lesson') == (
        'http://dummy.test/model/web/Page/'
        + '?course_slug=courses/minimal'
        + '&lesson_slug=any/lesson'
        + '&page_slug=index'
    )


def test_freeze_empty_course(empty_course):
    empty_course.freeze()
    check_empty_course_attrs(empty_course)


def test_get_lesson_url_freeze_error(empty_course):
    """Requested lessons are loaded on freeze(), failing if not available"""
    empty_course.get_lesson_url('any/lesson')
    empty_course.renderer = DummyRenderer()
    with pytest.raises(KeyError):
        empty_course.freeze()


def test_empty_course_from_renderer(model):
    """Valid trvial json that could come from a fork is loaded correctly"""
    source = 'courses/minimal/info.yml'
    renderer = DummyRenderer(
        course={
            'api_version': [0, 0],
            'course': {
                'title': 'A minimal course',
                'sessions': [],
                'source_file': source,
            }
        }
    )
    course = models.Course.load_local(
        parent=model,
        repo_info=get_local_repo_info('/dummy'),
        slug='courses/minimal',
        renderer=renderer,
    )
    check_empty_course_attrs(course, source_file=Path(source))
    assert_yaml_dump(models.dump(course), 'minimal-course.yml')
