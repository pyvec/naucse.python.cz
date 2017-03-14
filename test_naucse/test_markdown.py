from textwrap import dedent

from naucse.markdown_util import convert_markdown


def test_markdown_admonition():
    src = dedent("""
        !!! note ""
            Foo *bar*
    """)
    expected = '<div class="admonition note"><p>Foo <em>bar</em></p>\n</div>'
    assert convert_markdown(src) == expected


def test_markdown_admonition_paragraphs():
    src = dedent("""
        !!! note ""

            Foo *fi*

            fo

            fum
    """)
    expected = dedent("""
        <div class="admonition note"><p>Foo <em>fi</em></p>
        <p>fo</p>
        <p>fum</p>
        </div>
    """).strip()
    assert convert_markdown(src) == expected


def test_markdown_admonition_name():
    src = dedent("""
        !!! note "NB!"

            foo
    """)
    expected = dedent("""
        <div class="admonition note"><p class="admonition-title">NB!</p>
        <p>foo</p>
        </div>
    """).strip()
    assert convert_markdown(src) == expected
