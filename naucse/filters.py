import textwrap

from flask import g, request, url_for
from jinja2 import Markup

from naucse.routes import app
from naucse import markdown_util


@app.template_filter('markdown')
def convert_markdown(text, inline=False):
    return markdown_util.convert_markdown(text, inline=inline)


@app.template_filter('dedent')
def dedent(text):
    return textwrap.dedent(text)


@app.template_filter('extract_part')
def extract_part(text, part, delimiter):
    """Extract the given part of text. Parts are delimited by `delimiter`.

    Indexing starts at zero.
    """
    return text.split(delimiter)[part]


@app.template_filter('solution')
def solution(text):
    """A solution to a problem.

    The intent is for the solution to be hidden by default, and only shown
    after an explicit action by the reader.
    The explicit action can be:
    - Clicking a dumb link, which takes the reader to a special page that shows
      only the solution
    - Clicking a button, which shows the solution using Javascript

    To set up the special page, this filter needs special setup in the view.
    So, it can only be used within lesson pages.
    """
    solution_index = len(g.solutions)

    args = dict(request.view_args)
    args['solution'] = solution_index
    solution_url = url_for(request.url_rule.endpoint, **args)

    solution = markdown_util.convert_markdown(text)
    g.solutions.append(solution)

    t = Markup(textwrap.dedent("""
        <div class="solution" id="solution-{}">
            <h3>Řešení</h3>
            <div class="solution-cover">
                <a href="{}"><span class="link-text">Ukázat řešení</span></a>
            </div>
            <div class="solution-body" aria-hidden="true">
                {}
            </div>
        </div>
    """))
    return t.format(solution_index, solution_url, solution)
