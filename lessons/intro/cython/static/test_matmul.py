import pytest
import numpy

import matmul


@pytest.mark.parametrize(
    ('a', 'b', 'expected'),
    (
        (1, 1, 1),
        (3, 3, 9),
    )
)
def test_intmul(a, b, expected):
    assert matmul.intmul(a, b) == expected


@pytest.mark.parametrize(
    ('a', 'b', 'expected'),
    (
        ([[1, 0], [0, 1]], [[1, 2], [3, 4]], [[1, 2], [3, 4]]),
        ([[1, 2], [3, 4]], [[1, 0], [0, 1]], [[1, 2], [3, 4]]),
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),
        ([[1, 2, 3, 4]], [[5], [6], [7], [8]], [[70]]),
        ([[2]], [[3]], [[6]]),
    )
)
def test_matmul(a, b, expected):
    a = numpy.array(a)
    b = numpy.array(b)
    expected = numpy.array(expected)
    result = matmul.matmul(a, b)
    assert result.shape == (a.shape[0], b.shape[1])
    assert (result == expected).all()
