import calendar

from naucse import models


def test_2017_mipyt_zima_is_only_on_wednesdays():
    run = models.Course('.', 'runs/2017/mipyt-zima')
    for session in run.sessions.values():
        assert session.date.weekday() == calendar.WEDNESDAY
