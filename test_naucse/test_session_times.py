import datetime

import pytest
import dateutil.tz

from naucse import models
from test_naucse.conftest import fixture_path


TZINFO = dateutil.tz.gettz('Europe/Prague')


def test_run_with_times(model):
    model.load_local_courses(fixture_path / 'test_content')

    run = model.courses['2000/run-with-times']
    assert run.default_time == {
        'start': datetime.time(19, 00, tzinfo=TZINFO),
        'end': datetime.time(21, 00, tzinfo=TZINFO),
    }

    lesson = run.sessions['normal-lesson']
    assert lesson.date == datetime.date(2000, 1, 1)
    assert lesson.time == {
        'start': datetime.datetime(2000, 1, 1, 19, tzinfo=TZINFO),
        'end': datetime.datetime(2000, 1, 1, 21, tzinfo=TZINFO),
    }


def test_run_without_times(model):
    model.load_local_courses(fixture_path / 'test_content')

    run = model.courses['2000/run-without-times']
    assert run.default_time is None

    lesson = run.sessions['normal-lesson']
    assert lesson.date == datetime.date(2000, 1, 1)
    assert lesson.time is None


def test_course(model):
    model.load_local_courses(fixture_path / 'test_content')

    course = model.courses['courses/normal-course']
    assert course.default_time is None

    lesson = course.sessions['normal-lesson']
    assert lesson.date is None
    assert lesson.time is None
