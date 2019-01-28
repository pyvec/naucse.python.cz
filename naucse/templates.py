from jinja2 import Markup, StrictUndefined
import mistune

from .sanitize import sanitize_html

template_filters = {
    'sanitize': sanitize_html,
}


def template_filter(name=None):
    """Register a function as a Jinja template filter"""
    def _decorator(func):
        template_filters[name or func.__name__] = func
        return func
    return _decorator


def setup_jinja_env(jinja_env):
    """Sets up a Jinja environment with functions defined below"""
    jinja_env.filters.update(template_filters)
    jinja_env.undefined = StrictUndefined


@template_filter()
def markdown(text, inline=False):
    result = mistune.markdown(text)

    if inline:
        if not (result.startswith('<p>') and result.endswith('</p>')):
            raise ValueError('Inline Markdown not a paragraph: ' + result)
        result = result[len('<p>'):-len('</p>')]

    return Markup(result)


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
