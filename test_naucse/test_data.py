import calendar

from naucse import models


root = models.Root('.')


def test_2017_mipyt_zima_is_only_on_wednesdays():
    run = models.Course(root, 'runs/2017/mipyt-zima')
    for session in run.sessions.values():
        assert session.date.weekday() == calendar.WEDNESDAY


def test_2017_pyladies_praha_podzim_cznic_is_only_on_tuesdays():
    run = models.Course(root, 'runs/2017/pyladies-praha-podzim-cznic')
    for session in run.sessions.values():
        assert session.date.weekday() == calendar.TUESDAY
