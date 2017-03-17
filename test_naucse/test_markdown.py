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


def test_markdown_ansi_colors():
    src = dedent("""
        ```ansi
        On branch ansicolors
        Changes to be committed:
          (use "git reset HEAD <file>..." to unstage)

            ␛[32mmodified:   naucse/markdown_util.py␛[m

        Changes not staged for commit:
          (use "git add <file>..." to update what will be committed)
          (use "git checkout -- <file>..." to discard changes in working directory)

            ␛[31mmodified:   test_naucse/test_markdown.py␛[m
        ```
    """)
    expected = dedent("""
        <div class="codehilite"><pre><code>On branch ansicolors
        Changes to be committed:
          (use "git reset HEAD &lt;file&gt;..." to unstage)

            <span style="color: #00aa00">modified:   naucse/markdown_util.py</span>

        Changes not staged for commit:
          (use "git add &lt;file&gt;..." to update what will be committed)
          (use "git checkout -- &lt;file&gt;..." to discard changes in working directory)

            <span style="color: #aa0000">modified:   test_naucse/test_markdown.py</span></code></pre></div>
    """).strip()
    assert convert_markdown(src) == expected


def test_markdown_keeps_nbsp():
    text = 'Some text\N{NO-BREAK SPACE}more text'
    assert convert_markdown(text).strip() == '<p>{}</p>'.format(text)
