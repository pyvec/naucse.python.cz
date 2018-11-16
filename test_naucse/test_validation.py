from textwrap import dedent

import pytest

import naucse.sanitize
from naucse.sanitize import sanitize_html

def assert_changed(input_html, expected):
    input_html = dedent(input_html).strip()
    expected = dedent(expected).strip()
    output_html = sanitize_html(input_html)
    assert output_html == expected


def assert_unchanged(input_html):
    assert_changed(input_html, input_html)


def test_allowed_elements():
    # During the sanitization, content is parsed and re-rendered by LXML.
    # This does things like add the closing </strong> tag here.
    assert_changed(
        "<div><strong><u><a>Test</a></u></div>",
        "<div><strong><u><a>Test</a></u></strong></div>",
    )

def test_disallow_script():
    with pytest.raises(naucse.sanitize.DisallowedElement):
        sanitize_html(
            "<div><script>alert('XSS')</script></div>"
        )


def test_allow_attributes():
    assert_unchanged("""
        <div class="test">
            <span><a href="/courses/">Text</a></span>
        </div>
    """)

def test_disallow_onhover():
    with pytest.raises(naucse.sanitize.DisallowedAttribute):
        sanitize_html("""
            <div class="test" onhover="alert('XSS')">
                <a href="/courses/">Text</a>
            </div>
        """)

@pytest.mark.xfail
def test_disallow_unknown_css():
    with pytest.raises(naucse.sanitize.DisallowedStyle):
        sanitize_html("""
            <div class='test'>
                <span style='position: absolute; top: 0;'>Text</span>
            </div>
        """)

def test_disallow_javascript_href():
    with pytest.raises(naucse.sanitize.DisallowedURLScheme):
        sanitize_html(
            """<div class='test'><img src="javascript:alert('XSS')" /></div>"""
        )

def test_allowed_styles():
    assert_unchanged("""
        <style>
        .dataframe thead tr:only-child th {
            text-align: right;
        }

        </style>
    """)

def test_disallow_bad_css_syntax():
    with pytest.raises(naucse.sanitize.BadStyleSyntax):
        assert_unchanged("""
            <style>
            {
            </style>
        """)

def test_wrong_elements():
    with pytest.raises(naucse.sanitize.DisallowedStyle):
        sanitize_html("""
            <style>
            .green {
                color: green;
            }
            </style>
        """)

def test_bad_style():
    with pytest.raises(naucse.sanitize.DisallowedStyle):
        sanitize_html("""
            <style>
            .green {
                color: green
            </style>
        """)

def test_allow_multiple_css_selectors():
    assert_unchanged("""
        <style>
        .dataframe .green, .dataframe .also-green {
            color: green;
        }
        </style>
    """)

def test_invalid_multiple_css_selectors():
    with pytest.raises(naucse.sanitize.DisallowedStyle):
        sanitize_html("""
            <style>
            .dataframe .green, .also-green {
                color: green;
            }
            </style>
        """)
