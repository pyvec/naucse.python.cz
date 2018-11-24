import textwrap

import jinja2

from .markdown import convert_markdown

environment = jinja2.Environment(
    autoescape=jinja2.select_autoescape('html', 'xml'),
    undefined=jinja2.StrictUndefined,
)

def template_filter(name=None):
    def _decorator(func):
        environment.filters[name or func.__name__] = func
        return func
    return _decorator

def template_function(name=None):
    """Register a function as a Jinja template global"""
    def _decorator(func):
        environment.globals[name or func.__name__] = func
        return func
    return _decorator


@template_filter()
@jinja2.contextfilter
def markdown(ctx, text, inline=False):
    return ctx['$markdown'](text, inline=inline)


@template_filter()
def dedent(text):
    return textwrap.dedent(text)


@template_filter()
def extract_part(text, part, delimiter):
    """Extract the given part of text. Parts are delimited by `delimiter`.

    Indexing starts at zero.
    """
    return text.split(delimiter)[part]


@template_filter()
@jinja2.contextfilter
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

    solution_url = f'naucse:solution?solution={solution_index}'

    solution = ctx['$markdown'](text)
    solutions.append(solution)

    return jinja2.Markup(textwrap.dedent("""
        <div class="solution" id="solution-{}">
            <h3>Řešení</h3>
            <div class="solution-cover">
                <a href="{}"><span class="link-text">Ukázat řešení</span></a>
            </div>
            <div class="solution-body" aria-hidden="true">
                {}
            </div>
        </div>
    """).format(solution_index, solution_url, solution))


@template_function()
def var(name):
    """Return a page variable

    Variables are a mechanism for adapting lesson pages to the course
    or run they're part of.
    """
    # Templates that use vars should override this with `vars.get`.
    return None


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


@template_function()
def anchor(name):
    return jinja2.Markup('<a id="{}"></a>').format(name)


@template_function()
def figure(img, alt, float=None):
    classes = ['figure']
    if float == 'left':
        classes.append('float-left')
    elif float == 'right':
        classes.append('float-right')
    elif float is not None:
        raise ValueError('bad float: {}'.format(float))
    t = jinja2.Markup(''.join(p.strip() for p in """
        <span class="{classes}">
            <a href="{img}">
                <img src="{img}" alt="{alt}">
            </a>
        </span>
    """.splitlines()))
    return t.strip().format(img=img, alt=alt, classes=' '.join(classes))
