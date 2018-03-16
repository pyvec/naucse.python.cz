import textwrap
from pathlib import Path

from jinja2 import Markup, contextfilter

import naucse.utils.markdown


template_filters = {}


def template_filter(name=None):
    """Register a function as a Jinja template filter"""
    def _decorator(func):
        template_filters[name or func.__name__] = func
        return func
    return _decorator


template_globals = {}


def template_function(name=None):
    """Register a function as a Jinja template global"""
    def _decorator(func):
        template_globals[name or func.__name__] = func
        return func
    return _decorator


def setup_jinja_env(jinja_env):
    """Sets up a Jinja environment with functions defined below"""
    jinja_env.filters.update(template_filters)
    jinja_env.globals.update(template_globals)


@template_filter()
def markdown(text, inline=False):
    return naucse.utils.markdown.convert_markdown(text, inline=inline)


@template_filter()
def dedent(text):
    return textwrap.dedent(text)


@template_filter()
def edit_link(path):
    if path == Path("."):
        return "https://github.com/pyvec/naucse.python.cz"
    github_base = "https://github.com/pyvec/naucse.python.cz/blob/master/"
    return github_base + str(path)


@template_filter()
def extract_part(text, part, delimiter):
    """Extract the given part of text. Parts are delimited by `delimiter`.

    Indexing starts at zero.
    """
    return text.split(delimiter)[part]


@template_filter()
@contextfilter
def solution(ctx, text):
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
    solutions = ctx['$solutions']
    solution_index = len(solutions)

    solution_url = ctx['lesson_url'](lesson=ctx['lesson'].slug,
                                     page=ctx['page'].slug,
                                     solution=solution_index)

    solution = naucse.utils.markdown.convert_markdown(text)
    solutions.append(solution)

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


@template_function()
def var(name):
    """Return a page variable

    Variables are a mechanism for adapting lesson pages to the course
    or run they're part of.
    """
    # Templates that use vars should override this with `vars.get`.
    return None


@template_function()
def anchor(name):
    return Markup('<a id="{}"></a>').format(name)


@template_function()
def figure(img, alt, float=None):
    classes = ['figure']
    if float == 'left':
        classes.append('float-left')
    elif float == 'right':
        classes.append('float-right')
    elif float is not None:
        raise ValueError('bad float: {}'.format(float))
    t = Markup(''.join(p.strip() for p in """
        <span class="{classes}">
            <a href="{img}">
                <img src="{img}" alt="{alt}">
            </a>
        </span>
    """.splitlines()))
    return t.strip().format(img=img, alt=alt, classes=' '.join(classes))


def vars_functions(vars):
    if not vars:
        vars = {}

    def gnd(m, f, *, both=None):
        """Return `m` or `f` based on the user's grammatical gender

        If the gender is not known, return `both`, or "m/f" if not given.
        """
        gender = vars.get('user-gender')
        if gender == 'm':
            return m
        elif gender == 'f':
            return f
        elif both is None:
            return '{}/{}'.format(m, f)
        else:
            return both

    class A:
        """Stringifies to "" or "a", depending on user's grammatical gender

        (Note for English speakers: This is needed to form the past participle
        of most verbs, which is quite common in tutorials.)
        """
        def __str__(self):
            return gnd('', 'a')

    return {
        'var': vars.get,
        'gnd': gnd,
        'a': A(),
    }


@template_filter()
def format_time(time):
    if time.second:
        return '{d.hour}:{d.minute:02}:{d.second:02}'.format(d=time)
    return '{d.hour}:{d.minute:02}'.format(d=time)


@template_filter()
def format_date(date, relative_to=None):
    return '{d.day}. {d.month}. {d.year}'.format(d=date)


@template_filter()
def format_date_range(start_and_end):
    start, end = start_and_end
    parts = []
    if start != end:
        if start.year != end.year:
            parts += ['{start.day}. {start.month}. {start.year}']
        elif start.month != end.month:
            parts += ['{start.day}. {start.month}.']
        else:
            parts += ['{start.day}.']
        parts += [' – ']
    parts += [format_date(end)]
    return ''.join(parts).format(start=start, end=end)

@template_filter()
def monthname(number):
    return ('Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen', 'Červenec',
            'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec')[number-1]
