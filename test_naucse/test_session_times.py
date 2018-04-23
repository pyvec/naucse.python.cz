import datetime
from pathlib import Path

import pytest
import dateutil

from naucse import models


TZINFO = dateutil.tz.gettz('Europe/Prague')


@pytest.fixture
def model():
    path = Path(__file__).parent / 'fixtures/test_content'
    return models.Root(path)


def test_run_with_times(model):
    run = model.runs[2000, 'run-with-times']
    assert run.default_start_time == datetime.time(19, 00, tzinfo=TZINFO)
    assert run.default_end_time == datetime.time(21, 00, tzinfo=TZINFO)

    lesson = run.sessions['normal-lesson']
    assert lesson.date == datetime.date(2000, 1, 1)
    assert lesson.start_time == datetime.datetime(2000, 1, 1, 19, 00,
                                                  tzinfo=TZINFO)
    assert lesson.end_time == datetime.datetime(2000, 1, 1, 21, 00,
                                                tzinfo=TZINFO)


def test_run_without_times(model):
    run = model.runs[2000, 'run-without-times']
    assert run.default_start_time is None
    assert run.default_end_time is None

    lesson = run.sessions['normal-lesson']
    assert lesson.date == datetime.date(2000, 1, 1)
    assert lesson.start_time is None
    assert lesson.end_time is None


def test_course(model):
    course = model.courses['normal-course']
    assert course.default_start_time is None
    assert course.default_end_time is None

    lesson = course.sessions['normal-lesson']
    assert lesson.date is None
    assert lesson.start_time is None
    assert lesson.end_time is None
