import datetime

import pytest
import dateutil.tz

from naucse import models
from test_naucse.conftest import fixture_path, add_test_course


TZINFO = dateutil.tz.gettz('Europe/Prague')


def test_run_with_times(model):
    add_test_course(model, 'courses/with-times', {
        'title': 'Test course with scheduled times',
        'default_time': {'start': '19:00', 'end': '21:00'},
        'sessions': [
            {
                'title': 'A normal session',
                'slug': 'normal-session',
                'date': '2000-01-01',
            },
        ],
    })

    course = model.courses['courses/with-times']
    assert course.default_time == {
        'start': datetime.time(19, 00, tzinfo=TZINFO),
        'end': datetime.time(21, 00, tzinfo=TZINFO),
    }

    session = course.sessions['normal-session']
    assert session.date == datetime.date(2000, 1, 1)
    assert session.time == {
        'start': datetime.datetime(2000, 1, 1, 19, tzinfo=TZINFO),
        'end': datetime.datetime(2000, 1, 1, 21, tzinfo=TZINFO),
    }


def test_course_with_date_and_no_times(model):
    add_test_course(model, 'courses/without-times', {
        'title': 'Test course without scheduled times',
        'sessions': [
            {
                'title': 'A normal session',
                'slug': 'normal-session',
                'date': '2000-01-01',
            },
        ],
    })

    course = model.courses['courses/without-times']
    assert course.default_time is None

    session = course.sessions['normal-session']
    assert session.date == datetime.date(2000, 1, 1)
    assert session.time is None


def test_course_without_date(model):
    add_test_course(model, 'courses/without-dates', {
        'title': 'A plain vanilla course',
        'sessions': [
            {
                'title': 'A normal session',
                'slug': 'normal-session',
            },
        ],
    })

    course = model.courses['courses/without-dates']
    assert course.default_time is None

    session = course.sessions['normal-session']
    assert session.date is None
    assert session.time is None
