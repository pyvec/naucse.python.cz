import pytest

from test_naucse.conftest import assert_yaml_dump, add_test_course

@pytest.fixture
def empty_course(model):
    add_test_course(model, 'courses/minimal', {
        'title': 'A minimal course',
        'sessions': [],
    })
    return model.courses['courses/minimal']


def check_empty_course_attrs(empty_course):
    assert empty_course.slug == 'courses/minimal'
    assert empty_course.parent == empty_course.root
    assert empty_course.title == 'A minimal course'
    assert empty_course.subtitle == None
    assert empty_course.description == None
    assert empty_course.long_description == ''
    assert empty_course.vars == {}
    assert empty_course.place == None
    assert empty_course.time == None
    assert empty_course.default_time == None
    assert empty_course.sessions == {}
    assert empty_course.source_file == None
    assert empty_course.start_date == None
    assert empty_course.end_date == None
    assert empty_course.derives == None
    assert empty_course.base_course == None
    assert empty_course.get_recent_derived_runs() == []


def test_empty_course_attrs(model, empty_course):
    assert empty_course.root == model
    check_empty_course_attrs(empty_course)


def test_get_lesson_url_error(empty_course):
    assert empty_course.get_lesson_url('any/lesson') == (
        'http://dummy.test/model/web/Page/'
        + '?course_slug=courses/minimal'
        + '&lesson_slug=any/lesson'
        + '&page_slug=index'
    )


def test_freeze_empty_course(empty_course):
    empty_course.freeze()
    check_empty_course_attrs(empty_course)
