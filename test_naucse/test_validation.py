import pytest

import naucse.validation


def test_allowed_elements():
    allowed_elements = naucse.validation.AllowedElementsParser()

    allowed_elements.reset_and_feed(
        "<div><strong><u><a>Test</a></u></div>"
    )

    with pytest.raises(naucse.validation.DisallowedElement):
        allowed_elements.reset_and_feed(
            "<div><script>alert('XSS')</script></div>"
        )


def test_allowed_styles():
    allowed_elements = naucse.validation.AllowedElementsParser()

    allowed_elements.reset_and_feed(
        """
        <style>
        .dataframe thead tr:only-child th {
            text-align: right;
        }

        </style>
        """
    )

    # valid styles, but wrong elements
    with pytest.raises(naucse.validation.DisallowedStyle):
        allowed_elements.reset_and_feed(
            """
            <style>
            .green {
                color: green;
            }
            </style>
            """
        )

    # can't parse
    with pytest.raises(naucse.validation.DisallowedStyle):
        allowed_elements.reset_and_feed(
            """
            <style>
            .green {
                color: green
            </style>
            """
        )

    # multiple selectors in one rule
    # valid:
    allowed_elements.reset_and_feed(
        """
        <style>
        .dataframe .green, .dataframe .also-green {
            color: green;
        }
        </style>
        """
    )

    # invalid:
    with pytest.raises(naucse.validation.DisallowedStyle):
        allowed_elements.reset_and_feed(
            """
            <style>
            .dataframe .green, .also-green {
                color: green;
            }
            </style>
            """
        )
