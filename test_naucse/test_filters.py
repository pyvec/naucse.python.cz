from datetime import date

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
    )
)
def test_format_date_range(start, end, result):
    assert naucse.templates.format_date_range((start, end)) == result

