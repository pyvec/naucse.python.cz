import calendar

from naucse import models

import pytest


root = models.Root('.')


@pytest.mark.parametrize(('slug', 'weekday'), [
                             ('runs/2017/mipyt-zima',
                              calendar.WEDNESDAY),
                             ('runs/2017/pyladies-praha-podzim-cznic',
                              calendar.TUESDAY),
                             ('runs/2017/pyladies-praha-podzim-ntk',
                              calendar.MONDAY),
                         ])
def test_run_is_only_on_given_weekday(slug, weekday):
    run = models.Course(root, slug)
    for session in run.sessions.values():
        assert session.date.weekday() == weekday
