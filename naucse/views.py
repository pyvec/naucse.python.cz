import datetime
from pathlib import Path
import calendar

from flask import Flask, render_template, jsonify, url_for, Response
from werkzeug.local import LocalProxy
import ics

from naucse import models
from naucse.urlconverters import register_url_converters
from naucse.templates import setup_jinja_env

app = Flask('naucse')
app.config['JSON_AS_ASCII'] = False


_cached_model = None

def external_url_for(*args, **kwargs):
    return url_for(*args, **kwargs, _external=True)

@LocalProxy
def model():
    """Return the root of the naucse model

    In debug mode (elsa serve), a new model is returned for each requests,
    so changes are picked up.

    In non-debug mode (elsa freeze), a single model is used (and stored in
    _cached_model), so that metadata is only read once.
    """
    global _cached_model
    if _cached_model:
        return _cached_model
    model = models.Root(
        urls={
            'api': {
                models.Root: lambda r: external_url_for('api'),
                models.Course: lambda c: external_url_for(
                    'course_api', course=c),
                models.RunYear: lambda ry: external_url_for(
                    'run_year_api', year=ry.year),
            },
            'web': {
                models.Page: lambda p: external_url_for(
                    'page', material=p.material, page_slug=p.slug),
                models.Course: lambda c: external_url_for('course', course=c),
                models.Session: lambda s: external_url_for(
                    'session', course=s.course, session_slug=s.slug),
            },
            'schema': lambda m: external_url_for(
                'schema', model_name=m.__name__),
        },
    )
    model.load_local(Path(app.root_path).parent)
    if not app.config['DEBUG']:
        _cached_model = model
    return model

register_url_converters(app, model)
setup_jinja_env(app.jinja_env, model=model)


@app.route('/')
def index():
    # XXX: Edit URL
    return render_template("index.html", edit_info=model.edit_info)


@app.route('/courses/')
def courses():
    # XXX: Edit URL
    return render_template("course_list.html",
                           courses=model.courses,
                           title="Seznam online kurzů Pythonu")


@app.route('/runs/')
@app.route('/<int:year>/')
@app.route('/runs/<any(all):all>/')
def runs(year=None, all=None):
    # XXX: Simplify?
    today = datetime.date.today()

    # List of years to show in the pagination
    # If the current year is not there (no runs that start in the current year
    # yet), add it manually
    all_years = model.run_years.keys()
    if today.year not in all_years:
        all_years.append(today.year)
    first_year, last_year = min(all_years), max(all_years)

    if year is not None:
        if year > last_year:
            # Instead of showing a future year, redirect to the 'Current' page
            return redirect(url_for('runs'))
        if year not in all_years:
            # Otherwise, if there are no runs in requested year, return 404.
            abort(404)

    if all is not None:
        run_data = model.run_years

        paginate_prev = {'year': first_year}
        paginate_next = {'all': 'all'}
    elif year is None:
        # Show runs that are either ongoing or ended in the last 3 months
        runs = (model.runs_from_year(today.year) +
                model.runs_from_year(today.year - 1) +
                model.runs_from_year(today.year - 2))
        ongoing = [run for run in runs if run.end_date >= today]
        cutoff = today - datetime.timedelta(days=3*31)
        recent = [run for run in runs if today > run.end_date > cutoff]
        run_data = {"ongoing": ongoing, "recent": recent}

        paginate_prev = {'year': None}
        paginate_next = {'year': last_year}
    else:
        run_data = {year: [run for run
                           in model.runs_from_year(year) +
                              model.runs_from_year(year - 1)
                           if run.end_date.year >= year]}

        past_years = [y for y in all_years if y < year]
        if past_years:
            paginate_next = {'year': max(past_years)}
        else:
            paginate_next = {'all': 'all'}

        future_years = [y for y in all_years if y > year]
        if future_years:
            paginate_prev = {'year': min(future_years)}
        else:
            paginate_prev = {'year': None}

    return render_template("run_list.html",
                           run_data=run_data,
                           title="Seznam offline kurzů Pythonu",
                           today=datetime.date.today(),
                           year=year,
                           all=all,
                           all_years=all_years,
                           paginate_next=paginate_next,
                           paginate_prev=paginate_prev)


@app.route('/<course:course>/')
def course(course, year=None):
    #content = course_content(course)
    #allowed_elements_parser.reset_and_feed(content)

    kwargs = {
    #    "course_content": content,
    }

    #recent_runs = get_recent_runs(course)

    return render_template(
        "course.html",
        course=course,
        title=course.title,
        recent_runs=[], # XXX
        **kwargs
    )


@app.route('/<course:course>/sessions/<session_slug>/', defaults={'coverpage': 'front'})
@app.route('/<course:course>/sessions/<session_slug>/<coverpage>/')
def session(course, session_slug, coverpage):
    session = course.sessions[session_slug]

    kwargs = {
    #    "course_content": content,
    }

    #recent_runs = get_recent_runs(course)

    return render_template(
        "coverpage.html",
        course=course,
        session=session,
        title=course.title,
        content=None, # XXX
        **kwargs
    )


@app.route('/<material:material>/', defaults={'page_slug': 'index'})
@app.route('/<material:material>/<page_slug>/')
@app.route('/<material:material>/<page_slug>/solutions/<int:solution>/')
def page(material, page_slug='index', solution=None):
    page = material.pages[page_slug]

    kwargs = {}

    #lesson_url, subpage_url, static_url = relative_url_functions(request.path, course, lesson)
    #page, session, prv, nxt = get_page(course, lesson, page)

    #content = page_content(
    #    lesson, page, solution, course=course, lesson_url=lesson_url, subpage_url=subpage_url, static_url=static_url
    #)
    #content = content["content"]
    # XXX allowed_elements_parser.reset_and_feed(content)
    title = material.title

    #kwargs["edit_info"] = get_edit_info(page.edit_path)

    if solution is not None:
        kwargs["solution_number"] = int(solution)

    return render_template(
        "lesson.html",
        title=title,
        content='', # XXX,
        page=page,
        solution=solution,
        session=session,
        **kwargs
    )


def list_months(start_date, end_date):
    """Return a span of months as a list of (year, month) tuples

    The months of start_date and end_date are both included.
    """
    months = []
    year = start_date.year
    month = start_date.month
    while (year, month) <= (end_date.year, end_date.month):
        months.append((year, month))
        month += 1
        if month > 12:
            month = 1
            year += 1
    return months


@app.route('/<course:course>/calendar/')
def course_calendar(course):
    if not course.start_date:
        abort(404)

    sessions_by_date = {s.date: s for s in course.sessions.values()}

    kwargs = {
        "course": course,
        #"edit_info": get_edit_info(course.edit_path),
        'sessions_by_date': sessions_by_date,
        'months': list_months(course.start_date, course.end_date),
        'calendar': calendar.Calendar(),
    }

    return render_template('course_calendar.html', **kwargs)


def generate_calendar_ics(course):

    return ics.Calendar(events=events)


@app.route('/<course:course>/calendar.ics')
def course_calendar_ics(course):
    if not course.start_date:
        # No sessions with a date!
        abort(404)

    events = []
    for session in course.sessions.values():
        if session.start_time:
            start_time = session.start_time
            end_time = session.end_time
        else:
            # Sessions without times don't show up in the calendar
            continue

        cal_event = ics.Event(
            name=session.title,
            begin=start_time,
            end=end_time,
            uid=url_for("session_coverpage",
                        course=course,
                        session=session.slug,
                        _external=True),
        )
        events.append(cal_event)

    cal = ics.Calendar(events=events)
    return Response(str(cal), mimetype="text/calendar")


@app.route('/v1/schema.json', defaults={'model_name': 'Root'})
@app.route('/v1/schema/<model_name>.json')
def schema(model_name):
    try:
        cls = models.models[model_name]
    except KeyError:
        abort(404)
    return jsonify(models.get_schema(cls))


@app.route('/v1/naucse.json')
def api():
    return jsonify(model.dump(schema=True))


@app.route('/v1/years/<int:year>.json')
def run_year_api(year):
    return jsonify(model.run_years[year].dump(schema=True))


@app.route('/v1/<course:course>.json')
def course_api(course):
    return jsonify(course.dump(schema=True))
