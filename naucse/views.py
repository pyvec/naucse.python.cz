import datetime
from pathlib import Path
import calendar

from flask import Flask, render_template, jsonify, url_for, Response, abort
from flask import send_from_directory
from werkzeug.local import LocalProxy
import ics

from naucse import models
from naucse.urlconverters import register_url_converters
from naucse.templates import setup_jinja_env

app = Flask('naucse')
app.config['JSON_AS_ASCII'] = False


_cached_model = None


@LocalProxy
def model():
    """Return the root of the naucse model

    In debug mode (elsa serve), a new model is returned for each request,
    so changes are picked up.

    In non-debug mode (elsa freeze), a single model is used (and stored in
    _cached_model), so that metadata is only read once.
    """
    global _cached_model
    if _cached_model:
        return _cached_model
    model = models.Root(
        url_factories={
            'api': {
                models.Root: lambda r, **kw: url_for('api', **kw),
                models.Course: lambda c, **kw: url_for(
                    'course_api', course=c, **kw),
                models.RunYear: lambda ry, **kw: url_for(
                    'run_year_api', year=ry.year, **kw),
            },
            'web': {
                models.Page: lambda p, **kw: url_for(
                    'page', material=p.material, page_slug=p.slug, **kw),
                models.Solution: lambda s, **kw: url_for(
                    'page', material=s.page.material,
                    page_slug=s.page.slug, solution=s.index, **kw),
                models.Course: lambda c, **kw: url_for(
                    'course', course=c, **kw),
                models.Session: lambda s, **kw: url_for(
                    'session', course=s.course, session_slug=s.slug, **kw),
                models.SessionPage: lambda sp, **kw: url_for(
                    'session', course=sp.course, session_slug=sp.session.slug,
                    page=sp.slug, **kw),
                models.StaticFile: lambda sf, **kw: url_for(
                    'page_static', material=sf.material,
                    filename=sf.filename, **kw),
                models.Root: lambda r, **kw: url_for('index', **kw)
            },
        },
        schema_url_factory=lambda m, is_input, **kw: url_for(
                'schema', model_name=m.__name__, is_input=is_input, **kw),
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
    return render_template(
        "course_list.html",
        courses=model.courses,
    )


@app.route('/runs/')
@app.route('/<int:year>/')
@app.route('/runs/<any(all):all>/')
def runs(year=None, all=None):
    # XXX: Simplify?
    today = datetime.date.today()

    # List of years to show in the pagination
    # If the current year is not there (no runs that start in the current year
    # yet), add it manually
    all_years = list(model.run_years.keys())
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

    return render_template(
        "run_list.html",
        run_data=run_data,
        today=datetime.date.today(),
        year=year,
        all=all,
        all_years=all_years,
        paginate_next=paginate_next,
        paginate_prev=paginate_prev,
        edit_info=model.runs_edit_info,
    )


@app.route('/<course:course>/')
def course(course, year=None):
    kwargs = {
    #    "course_content": content,
    }

    #recent_runs = get_recent_runs(course)

    return render_template(
        "course.html",
        course=course,
        recent_runs=[], # XXX
        edit_info=course.get_edit_info(),
        **kwargs
    )


@app.route('/<course:course>/sessions/<session_slug>/', defaults={'page': 'front'})
@app.route('/<course:course>/sessions/<session_slug>/<page>/')
def session(course, session_slug, page):
    session = course.sessions[session_slug]

    #recent_runs = get_recent_runs(course)

    return render_template(
        "coverpage.html",
        session=session,
        course=session.course,
        edit_info=session.get_edit_info(),
        content=None, # XXX
    )


@app.route('/<material:material>/', defaults={'page_slug': 'index'})
@app.route('/<material:material>/<page_slug>/')
@app.route('/<material:material>/<page_slug>/solutions/<int:solution>/')
def page(material, page_slug='index', solution=None):
    try:
        page = material.pages[page_slug]
    except KeyError:
        raise abort(404)

    kwargs = {}

    # Get canonical URL -- i.e., a lesson with the same slug
    # XXX: This could be made much more fancy
    try:
        canonical = model.get_course('lessons').get_material(material.slug)
    except KeyError:
        canonical_url = None
    else:
        canonical_url = canonical.get_url(external=True)

    if solution is None:
        content = page.get_content()
    else:
        kwargs["solution_number"] = int(solution)
        solution = page.solutions[solution]
        content = solution.get_content()

    return render_template(
        "lesson.html",
        content=content,
        page=page,
        solution=solution,
        session=page.material.session,
        course=page.material.course,
        canonical_url=canonical_url,
        page_attribution=page.attribution,
        edit_info=page.get_edit_info(),
        **kwargs
    )


@app.route('/<material:material>/static/<path:filename>')
def page_static(material, filename):
    try:
        static = material.static_files[filename]
    except KeyError:
        raise abort(404)

    return send_from_directory(*static.get_file_info())


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

    sessions_by_date = {
        s.date: s for s in course.sessions.values()
        if hasattr(s, 'date')
    }

    return render_template(
        'course_calendar.html',
        course=course,
        sessions_by_date=sessions_by_date,
        months=list_months(course.start_date, course.end_date),
        calendar=calendar.Calendar(),
        edit_info=course.get_edit_info(),
    )


def generate_calendar_ics(course):

    return ics.Calendar(events=events)


@app.route('/<course:course>/calendar.ics')
def course_calendar_ics(course):
    if not course.start_date:
        # No sessions with a date!
        abort(404)

    events = []
    for session in course.sessions.values():
        if getattr(session, 'start_time', None):  # XXX
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


@app.route('/v1/schema/<is_input:is_input>.json', defaults={'model_name': 'Root'})
@app.route('/v1/schema/<is_input:is_input>/<model_name>.json')
def schema(model_name, is_input):
    try:
        cls = models.models[model_name]
    except KeyError:
        abort(404)
    return jsonify(models.get_schema(cls, is_input=is_input))


@app.route('/v1/naucse.json')
def api():
    return jsonify(model.dump())


@app.route('/v1/years/<int:year>.json')
def run_year_api(year):
    return jsonify(model.run_years[year].dump())


@app.route('/v1/<course:course>.json')
def course_api(course):
    return jsonify(course.dump())
