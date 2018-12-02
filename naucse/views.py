import datetime
from pathlib import Path
import functools
import calendar
import os

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
                    'course_api', course_slug=c.slug, **kw),
                models.RunYear: lambda ry, **kw: url_for(
                    'run_year_api', year=ry.year, **kw),
            },
            'web': {
                models.Lesson: lambda l, **kw: url_for(
                    'page', course_slug=l.course.slug, lesson_slug=l.slug,
                    page_slug='index', **kw),
                models.Page: lambda p, **kw: url_for(
                    'page', course_slug=p.course.slug,
                    lesson_slug=p.lesson.slug, page_slug=p.slug, **kw),
                models.Solution: lambda s, **kw: url_for(
                    'solution', course_slug=s.course.slug,
                    lesson_slug=s.lesson.slug,
                    page_slug=s.page.slug, index=s.index, **kw),
                models.Course: lambda c, **kw: url_for(
                    'course', course_slug=c.slug, **kw),
                models.Session: lambda s, **kw: url_for(
                    'session', course_slug=s.course.slug, session_slug=s.slug,
                    **kw),
                models.SessionPage: lambda sp, **kw: url_for(
                    'session', course_slug=sp.course.slug,
                    session_slug=sp.session.slug,
                    page=sp.slug, **kw),
                models.StaticFile: lambda sf, **kw: url_for(
                    'page_static', course_slug=sf.course.slug,
                    lesson_slug=sf.lesson.slug,
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
    return render_template("index.html", edit_info=model.edit_info)


@app.route('/courses/')
def courses():
    return render_template(
        "course_list.html",
        featured_courses=model.featured_courses,
        edit_info=model.course_edit_info,
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


@app.route('/<course:course_slug>/')
def course(course_slug, year=None):
    try:
        course = model.courses[course_slug]
    except KeyError:
        print(model.courses)
        abort(404)

    #recent_runs = get_recent_runs(course)

    return render_template(
        "course.html",
        course=course,
        recent_runs=[], # XXX
        edit_info=course.edit_info,
    )


@app.route('/<course:course_slug>/sessions/<session_slug>/',
              defaults={'page': 'front'})
@app.route('/<course:course_slug>/sessions/<session_slug>/<page>/')
def session(course_slug, session_slug, page):
    try:
        course = model.courses[course_slug]
        session = course.sessions[session_slug]
    except KeyError:
        abort(404)

    #recent_runs = get_recent_runs(course)

    template = {
        'front': 'coverpage.html',
        'back': 'backpage.html',
    }[page]

    materials_by_type = {}
    for material in session.materials:
        materials_by_type.setdefault(material.type, []).append(material)

    return render_template(
        template,
        session=session,
        course=session.course,
        edit_info=session.edit_info,
        materials_by_type=materials_by_type,
        content=None, # XXX
    )


def _get_canonicality_info(lesson):
    """Get canonical URL -- i.e., a lesson from 'lessons' with the same slug"""
    # XXX: This could be made much more fancy
    lessons_course = model.get_course('lessons')
    is_canonical_lesson = (lessons_course == lesson.course)
    if is_canonical_lesson:
        canonical_url = None
    else:
        try:
            canonical = lessons_course.lessons[lesson.slug]
        except KeyError:
            canonical_url = None
        else:
            canonical_url = canonical.get_url(external=True)
    return is_canonical_lesson, canonical_url


@app.route('/<course:course_slug>/<lesson:lesson_slug>/',
              defaults={'page_slug': 'index'})
@app.route('/<course:course_slug>/<lesson:lesson_slug>/<page_slug>/')
def page(course_slug, lesson_slug, page_slug='index'):
    try:
        course = model.courses[course_slug]
        lesson = course.lessons[lesson_slug]
        page = lesson.pages[page_slug]
    except KeyError:
        raise abort(404)

    is_canonical_lesson, canonical_url = _get_canonicality_info(lesson)

    return render_template(
        "lesson.html",
        page=page,
        content=page.content,
        course=course,
        canonical_url=canonical_url,
        is_canonical_lesson=is_canonical_lesson,
        page_attribution=page.attribution,
        edit_info=page.edit_info,
    )


@app.route('/<course:course_slug>/<lesson:lesson_slug>/<page_slug>'
              + '/solutions/<int:index>/')
def solution(course_slug, lesson_slug, page_slug, index):
    try:
        course = model.courses[course_slug]
        lesson = course.lessons[lesson_slug]
        page = lesson.pages[page_slug]
        solution = page.solutions[index]
    except KeyError:
        raise abort(404)

    is_canonical_lesson, canonical_url = _get_canonicality_info(lesson)

    return render_template(
        "lesson.html",
        page=page,
        content=solution.content,
        course=course,
        canonical_url=canonical_url,
        is_canonical_lesson=is_canonical_lesson,
        page_attribution=page.attribution,
        edit_info=page.edit_info,
        solution_number=index,
    )


@app.route('/<course:course_slug>/<lesson:lesson_slug>/static/<path:filename>')
def page_static(course_slug, lesson_slug, filename):
    try:
        course = model.courses[course_slug]
        lesson = course.lessons[lesson_slug]
        static = lesson.static_files[filename]
    except KeyError:
        raise abort(404)

    print('sending', static.base_path, static.filename)
    return send_from_directory(static.base_path, static.path)


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


@app.route('/<course:course_slug>/calendar/')
def course_calendar(course_slug):
    try:
        course = model.courses[course_slug]
    except KeyError:
        abort(404)

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
        edit_info=course.edit_info,
    )


def generate_calendar_ics(course):

    return ics.Calendar(events=events)


@app.route('/<course:course_slug>/calendar.ics')
def course_calendar_ics(course_slug):
    try:
        course = model.courses[course_slug]
    except KeyError:
        abort(404)

    if not course.start_date:
        abort(404)

    events = []
    for session in course.sessions.values():
        if getattr(session, 'start_time', None):  # XXX
            start_time = session.start_time
            end_time = session.end_time
        else:
            # Sessions without times don't show up in the calendar
            continue

        created = os.environ.get('NAUCSE_CALENDAR_DTSTAMP', None)
        cal_event = ics.Event(
            name=session.title,
            begin=start_time,
            end=end_time,
            uid=session.get_url(external=True),
            created=created,
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
    return jsonify(models.dump(model, models.Root))


@app.route('/v1/years/<int:year>.json')
def run_year_api(year):
    try:
        run_year = model.courses[model.run_years[year]]
    except KeyError:
        abort(404)
    return jsonify(models.dump(run_year))


@app.route('/v1/<course:course_slug>.json')
def course_api(course_slug):
    try:
        course = model.courses[course_slug]
    except KeyError:
        abort(404)
    return jsonify(models.dump(course))
