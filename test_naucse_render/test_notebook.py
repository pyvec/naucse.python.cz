from textwrap import dedent
from pathlib import Path

import click
import pygments

import pytest

from naucse_render.notebook import convert_notebook


FIXTURES = Path(__file__).parent / 'fixtures'


@pytest.fixture(scope='module')
def _notebook():
    path = FIXTURES / 'notebook.ipynb'
    with open(path) as f:
        content = f.read()
    return convert_notebook(content)


@pytest.fixture()
def notebook(_notebook):
    click.echo(pygments.highlight(
        _notebook,
        lexer=pygments.lexers.get_lexer_by_name('html'),
        formatter=pygments.formatters.get_formatter_by_name('console')
    ))
    return _notebook


def test_notebook_markdown_cell_conversion(notebook):
    markdown = dedent(r"""
        <h2>Markdown</h2>
        <p>This is <em>Markdown cell</em>!</p>
        <p>It even has some $\LaTeX$:</p>
        <p>$$ x = \sin(\pi) $$</p>
    """).strip()
    assert markdown in notebook


def test_notebook_has_input_prompt(notebook):
    input_prompt = '<div class="prompt input_prompt">In&nbsp;[1]:</div>'
    assert input_prompt in notebook


def test_notebook_has_output_prompt(notebook):
    input_prompt = '<div class="prompt output_prompt">Out[1]:</div>'
    assert input_prompt in notebook


def test_notebook_has_highlighted_input_area(notebook):
    input_area = dedent("""
        <div class=" highlight hl-ipython3">
        <pre>
        <span></span><span class="nb">print</span><span class="p">(</span>
        <span class="s1">&#39;foo&#39;</span><span class="p">)</span>
        <span class="mi">5</span> <span class="o">+</span>
         <span class="mi">2</span>
        </pre>
        </div>
    """).strip().replace('\n', '')
    assert input_area in notebook.replace('\n', '')


@pytest.mark.parametrize('output', ('foo', 7))
def test_notebook_has_desired_outputs(notebook, output):
    output_pre = '<pre>{}</pre>'.format(output)
    assert output_pre in notebook.replace('\n', '')
