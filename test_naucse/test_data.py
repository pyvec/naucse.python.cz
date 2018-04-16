import calendar
from pathlib import Path

from naucse import models

import pytest

path = Path(__file__).parent / 'fixtures/test_content'
root = models.Root(path)


@pytest.mark.parametrize(('slug', 'weekday'), [
                             ('runs/2000/run-wednesdays',
                              calendar.WEDNESDAY),
                             ('runs/2000/run-tuesdays',
                              calendar.TUESDAY),
                             ('runs/2000/run-mondays',
                              calendar.MONDAY),
                         ])
def test_run_is_only_on_given_weekday(slug, weekday):
    run = models.Course(root, path / slug)
    for session in run.sessions.values():
        assert session.date.weekday() == weekday
