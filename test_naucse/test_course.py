from pathlib import Path

import pytest
import yaml
from jsonschema.exceptions import ValidationError

from naucse import models
from naucse.edit_info import get_local_repo_info

from test_naucse.conftest import add_test_course, fixture_path

class DummyRenderer:
    """Renderer that returns courses/lessons from the given data

    Mocks the get_lessons method of naucse_render or arca_renderer.Renderer.

    As `course`, DummyRenderer expects a full API response, complete with
    api_version.
    The `lessons` argument should be a mapping of lesson slugs to full API
    responses.

    As of now, get_lessons only allows a single lesson slug.
    """

    def __init__(self, course=None, lessons=None):
        self.course = course
        self._lessons = lessons or {}

    def get_course(self, slug, *, version, path):
        return self.course

    def get_lessons(self, lessons, *, vars, path):
        [slug] = lessons
        try:
            return self._lessons[slug]
        except KeyError as e:
            raise DummyLessonNotFound(slug) from e

class DummyLessonNotFound(LookupError):
    """Raised by DummyRenderer when a lesson is not found"""


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
    with pytest.raises(DummyLessonNotFound):
        empty_course.freeze()


def test_empty_course_from_renderer(model, assert_model_dump):
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
    assert_model_dump(course, 'minimal-course')


def load_course_from_fixture(model, filename):
    """Load course from a file with info as it would come from a fork.

    Contents of the file are passed as kwargs to DummyRenderer.
    """

    with (fixture_path / filename).open() as f:
        renderer = DummyRenderer(**yaml.safe_load(f))
    course = models.Course.load_local(
        parent=model,
        repo_info=get_local_repo_info('/dummy'),
        slug='courses/complex',
        renderer=renderer,
    )
    model.add_course(course)
    return course


def test_complex_course(model, assert_model_dump):
    """Valid complex json that could come from a fork is loaded correctly"""
    course = load_course_from_fixture(model, 'course-data/complex-course.yml')

    assert_model_dump(course, 'complex-course')

    # Make sure HTML is sanitized
    assert course.long_description == 'A <em>fun course!</em>'
    assert course.sessions['full'].description == 'A <em>full session!</em>'


def test_derives(model):
    """Test that derives and base_course is set correctly"""
    add_test_course(model, 'courses/base', {
        'title': 'A base course',
        'sessions': [],
    })
    add_test_course(model, 'courses/derived', {
        'title': 'A derived course',
        'sessions': [],
        'derives': 'base'
    })

    base = model.courses['courses/base']
    derived = model.courses['courses/derived']

    assert derived.derives == 'base'
    assert derived.base_course is base


def test_nonexisting_derives(model):
    """Test that nonexisting derives fails quietly"""
    add_test_course(model, 'courses/bad-derives', {
        'title': 'A course derived from nothing',
        'sessions': [],
        'derives': 'nonexisting'
    })

    course = model.courses['courses/bad-derives']

    assert course.derives == 'nonexisting'
    assert course.base_course is None


def test_invalid_course(model):
    """Invalid complex json that could come from a fork is not loaded"""
    with pytest.raises(ValidationError):
        load_course_from_fixture(model, 'course-data/invalid-course.yml')
