from datetime import date, time, datetime

import pytest

import naucse.templates


@pytest.mark.parametrize(
    ('start', 'end', 'result'),
    (
        (date(2017, 9, 25), date(2017, 9, 25), '25. 9. 2017'),
        (date(2017, 9, 1), date(2017, 9, 25), '1. – 25. 9. 2017'),
        (date(2017, 8, 1), date(2017, 9, 25), '1. 8. – 25. 9. 2017'),
        (date(2017, 8, 25), date(2017, 9, 25), '25. 8. – 25. 9. 2017'),
        (date(2016, 9, 25), date(2017, 9, 25), '25. 9. 2016 – 25. 9. 2017'),
        (datetime(2016, 9, 25, 8, 30), datetime(2017, 9, 25, 18, 0),
         '25. 9. 2016 – 25. 9. 2017'),
    )
)
def test_format_date_range(start, end, result):
    assert naucse.templates.format_date_range((start, end)) == result


@pytest.mark.parametrize(
    ('time', 'result'),
    (
        (time(8, 0, 0), '8:00'),
        (time(18, 0, 0), '18:00'),
        (time(8, 3, 0), '8:03'),
        (time(8, 3, 5), '8:03:05'),
        (time(18, 4, 5), '18:04:05'),
        (datetime(2018, 1, 14, 18, 4, 5), '18:04:05'),
    )
)
def test_format_time(time, result):
    assert naucse.templates.format_time(time) == result
