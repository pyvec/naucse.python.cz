from textwrap import dedent
import html

import pytest

from naucse_render.markdown import convert_markdown, style_space_after_prompt


def test_markdown_admonition():
    src = dedent("""
        > [note]
        > Foo *bar*
    """)
    expected = '<div class="admonition note"><p>Foo <em>bar</em></p>\n</div>'
    assert convert_markdown(src) == expected


def test_markdown_admonition_paragraphs():
    src = dedent("""
        > [note]
        >
        > Foo *fi*
        >
        > fo
        >
        > fum
    """)
    expected = dedent("""
        <div class="admonition note"><p>Foo <em>fi</em></p>
        <p>fo</p>
        <p>fum</p>
        </div>
    """).strip()
    assert convert_markdown(src) == expected


def test_markdown_admonition_name_and_title():
    src = dedent("""
        > [warning] NB!
        >
        > foo
    """)
    expected = dedent("""
        <div class="admonition warning"><p class="admonition-title">NB!</p>
        <p>foo</p>
        </div>
    """).strip()
    assert convert_markdown(src) == expected


def test_markdown_admonition_code():
    src = dedent("""
        > [note] NB!
        >
        > foo
        > ```python
        > cat = Kitty()
        > cat.make_sound()
        > ```
    """)
    expected = dedent("""
        <div class="admonition note"><p class="admonition-title">NB!</p>
        <p>foo</p>
        <div class="highlight"><pre><span></span><span class="n">cat</span> <span class="o">=</span> <span class="n">Kitty</span><span class="p">()</span>
        <span class="n">cat</span><span class="o">.</span><span class="n">make_sound</span><span class="p">()</span>
        </pre></div></div>
    """).strip()
    assert convert_markdown(src) == expected


def test_markdown_admonition_html():
    src = dedent("""
            > [note]
            > Foo <var>bar</var>
        """)
    expected = '<div class="admonition note"><p>Foo <var>bar</var></p>\n</div>'
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
        <div class="highlight"><pre><code>On branch ansicolors
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


@pytest.mark.parametrize('what', ('image', 'link'))
def test_static_link_conversion(what):
    text = '[alt](foo/bar)'
    if what == 'image':
        text = '!' + text

    def convert_url(url):
        return url[::-1]

    param = 'href' if what == 'link' else 'src'
    assert '{}="rab/oof"'.format(param) in convert_markdown(text, convert_url)


@pytest.fixture(params=['$', '(__venv__)$', '>>>', '...'])
def prompt(request):
    return request.param.replace('>', '&gt;')


def test_single_space_after_prompt(prompt):
    original = '<span class="gp">{}</span> foo'.format(prompt)
    expected = '<span class="gp">{} </span>foo'.format(prompt)
    assert style_space_after_prompt(original) == expected


def test_multiple_spaces_after_prompt(prompt):
    original = '<span class="gp">{}</span>     foo'.format(prompt)
    expected = '<span class="gp">{} </span>    foo'.format(prompt)
    assert style_space_after_prompt(original) == expected


def test_prompt_already_with_space(prompt):
    original = '<span class="gp">{} </span>foo'.format(prompt)
    assert style_space_after_prompt(original) == original


def test_prompt_already_with_space_extra_spaces(prompt):
    original = '<span class="gp">{} </span>    foo'.format(prompt)
    assert style_space_after_prompt(original) == original


def test_convert_with_prompt_spaces_pycon():
    src = dedent("""
        ```pycon
        >>> def foo(req):
        ...     return req
        ```
    """)
    expected = dedent("""
        <div class="highlight"><pre><span></span>
        <span class="gp">&gt;&gt;&gt; </span><span class="k">def</span>
         <span class="nf">foo</span><span class="p">(</span>
        <span class="n">req</span><span class="p">):</span>
        <span class="gp">... </span>
            <span class="k">return</span> <span class="n">req</span>
        </pre></div>
    """).strip().replace('\n', '')
    assert convert_markdown(src).replace('\n', '') == expected


def test_convert_with_prompt_spaces_console():
    src = dedent("""
        ```console
        (__venv__)$ python
        ```
    """)
    expected = dedent("""
        <div class="highlight"><pre><span></span>
        <span class="gp">(__venv__)$ </span>python
        </pre></div>
    """).strip().replace('\n', '')
    assert convert_markdown(src).replace('\n', '') == expected


@pytest.mark.parametrize('lexer', ('python', 'pycon'))
def test_convert_with_matrix_multiplication(lexer):
    src = dedent("""
        ```{}
        {}a @ a
        ```
    """.format(lexer, '>>> ' if lexer == 'pycon' else ''))
    expected = dedent("""
        <span class="n">a</span> <span class="o">@</span>
         <span class="n">a</span>
    """).strip().replace('\n', '')
    assert expected in convert_markdown(src).replace('\n', '')


@pytest.mark.parametrize('pre_prompt', ('', '(__venv__) ', '(env)'))
@pytest.mark.parametrize('space', ('', ' '))
@pytest.mark.parametrize('command', ('python', '07:28 PM <DIR> Desktop'))
def test_convert_with_dosvenv_prompt(pre_prompt, space, command):
    src = dedent("""
        ```dosvenv
        {}>{}{}
        ```
    """).format(pre_prompt, space, command)
    expected = dedent("""
        <div class="highlight"><pre><span></span>
        <span class="gp">{}&gt;{}</span>{}
        </pre></div>
    """).strip().replace('\n', '').format(pre_prompt, space, html.escape(command))
    assert convert_markdown(src).replace('\n', '') == expected


def test_convert_full_dosvenv_prompt():
    src = dedent(r"""
        ```dosvenv
        > whoami
        helena
        > venv\Scripts\activate  # activate virtualenv
        (venv)> dir
         Directory of C:\Users\helena
        05/08/2014 07:28 PM <DIR>  Desktop
        ```
    """)
    expected = dedent(r"""
        <div class="highlight"><pre><span></span><span class="gp">&gt; </span>whoami
        <span class="go">helena</span><span class="gp"></span>
        <span class="gp">&gt; </span>venv\Scripts\activate  <span class="c"># activate virtualenv</span>
        <span class="gp">(venv)&gt; </span>dir
        <span class="go"> Directory of C:\Users\helena</span>
        <span class="go">05/08/2014 07:28 PM &lt;DIR&gt;  Desktop</span>
        </pre></div>
    """).strip()
    print(expected)
    assert convert_markdown(src) == expected
