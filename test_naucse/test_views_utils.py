import datetime

import pytest

import naucse.views


@pytest.mark.parametrize(
    ['start', 'end', 'expected'],
    [
        (datetime.date(2016, 12, 3), datetime.date(2016, 12, 3),
         [(2016, 12)]),
        (datetime.date(2016, 12, 3), datetime.date(2016, 12, 23),
         [(2016, 12)]),
        (datetime.date(2016, 12, 3), datetime.date(2017, 1, 3),
         [(2016, 12), (2017, 1)]),
        (datetime.date(2016, 12, 3), datetime.date(2017, 5, 8),
         [(2016, 12), (2017, 1), (2017, 2), (2017, 3), (2017, 4), (2017, 5)]),
        (datetime.date(2016, 12, 3), datetime.date(2018, 1, 8),
         [(2016, 12), (2017, 1), (2017, 2), (2017, 3), (2017, 4), (2017, 5),
          (2017, 6), (2017, 7), (2017, 8), (2017, 9), (2017, 10), (2017, 11),
          (2017, 12), (2018, 1)]),
    ])
def test_list_months(start, end, expected):
    assert naucse.views.list_months(start, end) == expected
