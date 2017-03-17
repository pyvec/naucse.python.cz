from pathlib import Path

import click
import pygments

from naucse.models import Root


@click.command()
@click.argument('lesson')
@click.argument('page', default='index')
@click.option('-d', '--data',
              type=click.Path(file_okay=False, dir_okay=True, exists=True),
              help='Directory with the data')
@click.option('-s', '--solution', type=int,
              help='Instead of printing the whole text, print the given '
                   + 'solution')
def render(data, lesson, page, solution):
    """Renders the given lesson as a HTML fragment

    Example:
        python -m naucse.render beginners/variables
    """
    if data is None:
        data = Path(__file__).parent.parent

    model = Root(data)

    page = model.get_lesson(lesson).pages[page]

    result = page.render_html(solution=solution)

    click.echo(pygments.highlight(
        result,
        lexer=pygments.lexers.get_lexer_by_name('html'),
        formatter=pygments.formatters.get_formatter_by_name('console')
    ))

    click.secho('Note: This script is experimental; '
                + 'it may be renamed in the future',
                fg='red', err=True)


render()
