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


def test_markdown_definition_list():
    src = dedent("""
        Bla Bla

        The Term
        :    Its Definition

        More Text
    """)
    expected = dedent("""
        <p>Bla Bla</p>
        <dl>
        <dt></dt><dt>The Term</dt><dd><p>Its Definition</p>
        </dd></dl><p>More Text</p>
    """).strip()
    assert convert_markdown(src).strip() == expected


def test_markdown_definition_list_advanced():
    src = dedent("""
        Bla Bla

        The Term
        :   Its Definition
            More Definition

            Even More

        Another Term
        :   Define this

        More Text
    """)
    expected = dedent("""
        <p>Bla Bla</p>
        <dl>
        <dt></dt><dt>The Term</dt><dd><p>Its Definition
        More Definition</p>
        <p>Even More</p>
        </dd><dt></dt><dt>Another Term</dt><dd><p>Define this</p>
        </dd></dl><p>More Text</p>
    """).strip()
    print(convert_markdown(src))
    assert convert_markdown(src).strip() == expected
