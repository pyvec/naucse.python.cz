import datetime
import shutil
import tempfile
from collections import OrderedDict
from pathlib import Path

import pytest
import yaml
from arca.exceptions import BuildError
from flask.testing import FlaskClient
from git import Repo

from naucse import models
from naucse.utils.views import page_content_cache_key
from naucse.utils.models import arca


def generate_info(title, course_type, coach_present, some_var):
    return {
        "title": title,
        "description": f"{course_type} description",
        "long_description": f"{course_type} long description",
        "vars": {
            "coach-present": coach_present,
            "some-var": some_var
        },
        "plan": [
            {"title": "First session",
             "slug": "first-session",
             "materials": [
                 {"lesson": "beginners/cmdline"},
                 {"lesson": "beginners/install"},
             ]},
            {"title": "Second session",
             "slug": "second-session",
             "materials": [
                 {"lesson": "beginners/first-steps"},
                 {"lesson": "beginners/install-editor"},
             ]},
        ]
    }


def generate_course(title):
    return generate_info(title, "Course", False, True)


def generate_run(title):
    run = generate_info(title, "Run", True, False)
    run["default_time"] = {
        "start": "18:00",
        "end": "20:00"
    }
    run["plan"][0]["date"] = datetime.date(2018, 2, 6)
    run["plan"][1]["date"] = datetime.date(2018, 2, 8)

    return run


@pytest.fixture(scope="module")
def fork():
    """Generate a local fork of the current state of naucse for testing.

    1) Copies the entire local state of naucse
    2) Adds one working course and one working run
    3) Commits everything on branch ``test_branch``
    4) Adds one more course and one more run, but breaks all rendering
    5) Commits the broken state on ``test_broken_branch``
    6) Deletes the fork once pytest finishes using this fixture
    """

    # create a fork on a branch ``test_branch``
    def ignore(_, names):
        return [x for x in names
                if ((x.startswith(".") and x not in {".git", ".gitignore", ".travis.yml"}) or
                    x == "_build" or
                    x == "__pycache__")]

    test_dir = Path(tempfile.mkdtemp()) / "naucse"
    naucse = Path(__file__).parent.parent
    shutil.copytree(naucse, str(test_dir), ignore=ignore)

    repo = Repo(str(test_dir))
    branch = "test_branch"
    repo.create_head(branch)
    getattr(repo.heads, branch).checkout()

    # one working course
    course_info = test_dir / "courses/test-course/info.yml"
    course_info.parent.mkdir(exist_ok=True, parents=True)
    course_info.write_text(yaml.dump(generate_course("Course title"), default_flow_style=False))

    # one working run
    run_info = test_dir / "runs/2018/test-run/info.yml"
    run_info.parent.mkdir(exist_ok=True, parents=True)
    run_info.write_text(yaml.dump(generate_run("Run title"), default_flow_style=False))

    # commit everything
    repo.git.add([str(course_info), str(run_info)])
    repo.git.add(A=True)
    repo.index.commit("Commited everything")

    # a broken branch for error handling testing
    branch = "test_broken_branch"
    repo.create_head(branch)
    getattr(repo.heads, branch).checkout()

    course_broken_info = test_dir / "courses/test-broken-course/info.yml"
    course_broken_info.parent.mkdir(exist_ok=True, parents=True)
    course_broken_info.write_text(yaml.dump(generate_course("Broken course title"), default_flow_style=False))

    run_broken_info = test_dir / "runs/2018/test-broken-run/info.yml"
    run_broken_info.parent.mkdir(exist_ok=True, parents=True)
    run_broken_info.write_text(yaml.dump(generate_run("Broken run title"), default_flow_style=False))

    utils = test_dir / "naucse/utils" / "forks.py"
    utils.write_text("")

    repo.git.add([str(course_broken_info), str(run_broken_info), str(utils)])
    repo.index.commit("Created duplicates in a different branch, but broke rendering")

    yield f"file://{test_dir}"

    shutil.rmtree(test_dir.parent)


@pytest.fixture(scope="module")
def model(fork):
    """Generate a Root instance with the courses and runs generated in ``fork``
    """
    path = Path(__file__).parent / 'fixtures/test_content'
    root = models.Root(path)

    course = models.CourseLink(root, path / 'courses/test-course')
    course.repo = fork
    course.branch = 'test_branch'

    course_broken = models.CourseLink(root, path / 'courses/test-broken-course')
    course_broken.repo = fork
    course_broken.branch = 'test_broken_branch'

    run = models.CourseLink(root, path / 'runs/2018/test-run')
    run.repo = fork
    run.branch = 'test_branch'

    run_broken = models.CourseLink(root, path / 'runs/2018/test-broken-run')
    run_broken.repo = fork
    run_broken.branch = 'test_broken_branch'

    # so rendering still works
    meta = models.Course(root, path / 'courses/normal-course')
    meta.is_meta = True

    # so no file operations are needed, override list of courses and runs as well

    root.courses = OrderedDict([('test-course', course),
                                ('test-broken-course', course_broken),
                                ('meta', meta)])

    run_year = models.RunYear(root, path / 'runs/2018')
    run_year.runs = OrderedDict([
        ("test-run", run),
        ("test-broken-run", run_broken)
    ])

    root.run_years = OrderedDict([
        (2018, run_year)
    ])
    root.runs = {(2018, "test-run"): run, (2018, "test-broken-run"): run_broken}

    return root


@pytest.fixture
def client(model, mocker):
    """Generate a client for testing endpoints, model will be used.
    """
    # these methods have the @reify decorator, however we need for them to be recalculated
    # so ``naucse.utils.views.forks_enabled`` can be tested
    if hasattr(model, "safe_runs"):
        delattr(model, "safe_runs")
    if hasattr(model, "safe_run_years"):
        delattr(model, "safe_run_years")

    mocker.patch("naucse.views._cached_model", model)
    from naucse import app
    app.testing = True
    yield app.test_client()


def test_course_info(model):
    """Test that all course metadata is generated properly from the fork info
    """
    assert model.courses["test-course"].title == "Course title"
    assert model.courses["test-course"].description == "Course description"
    assert model.courses["test-course"].start_date is None
    assert model.courses["test-course"].end_date is None
    assert not model.courses["test-course"].canonical
    assert model.courses["test-course"].vars.get("coach-present") is False
    assert model.courses["test-course"].vars.get("some-var") is True


def test_run_info(model):
    """Test that all run meta data are generated properly from the fork info
    """
    assert model.runs[(2018, "test-run")].title == "Run title"
    assert model.runs[(2018, "test-run")].description == "Run description"
    assert model.runs[(2018, "test-run")].start_date == datetime.date(2018, 2, 6)
    assert model.runs[(2018, "test-run")].end_date == datetime.date(2018, 2, 8)
    assert not model.runs[(2018, "test-run")].canonical
    assert model.runs[(2018, "test-run")].vars.get("coach-present") is True
    assert model.runs[(2018, "test-run")].vars.get("some-var") is False


def test_course_render(model):
    """Test that non-run course pages are rendered correctly

    Tested pages are course, sessions, lessons.
    Also test that run pages (calendar) aren't rendered for non-run courses.
    """
    assert model.courses["test-course"].render_course()
    with pytest.raises(BuildError):
        model.courses["test-course"].render_calendar()

    with pytest.raises(BuildError):
        model.courses["test-course"].render_calendar_ics()

    assert model.courses["test-course"].render_session_coverpage("first-session", "front")
    assert model.courses["test-course"].render_session_coverpage("first-session", "back")

    index = model.courses["test-course"].render_page("beginners/cmdline", "index", None,
                                                     request_url="/course/test-course/beginners/cmdline/")
    assert index
    solution = model.courses["test-course"].render_page(
        "beginners/cmdline", "index", 0, request_url="/course/test-course/beginners/cmdline/index/solutions/0/"
    )
    assert solution
    assert index != solution

    index = model.courses["test-course"].render_page("beginners/install", "index", None,
                                                     request_url="/course/test-course/beginners/install/")
    assert index
    linux = model.courses["test-course"].render_page("beginners/install", "linux", None,
                                                     request_url="/course/test-course/beginners/install/linux/")
    assert linux
    assert index != linux


def test_run_render(model):
    """Test that run pages are rendered correctly

    Tested pages are course, calendars, sessions, lessons.
    """
    assert model.runs[(2018, "test-run")].render_course()

    assert model.runs[(2018, "test-run")].render_calendar()
    assert model.runs[(2018, "test-run")].render_calendar_ics()

    assert model.runs[(2018, "test-run")].render_session_coverpage("first-session", "front")
    assert model.runs[(2018, "test-run")].render_session_coverpage("first-session", "back")

    index = model.runs[(2018, "test-run")].render_page("beginners/cmdline", "index", None,
                                                       request_url="/2018/test-run/beginners/cmdline/")
    assert index
    solution = model.runs[(2018, "test-run")].render_page(
        "beginners/cmdline", "index", 0, request_url="/2018/test-run/beginners/cmdline/index/solutions/0/"
    )
    assert solution
    assert index != solution

    index = model.runs[(2018, "test-run")].render_page("beginners/install", "index", None,
                                                       request_url="/2018/test-run/beginners/install/")
    assert index
    linux = model.runs[(2018, "test-run")].render_page("beginners/install", "linux", None,
                                                       request_url="/2018/test-run/beginners/install/linux/")
    assert linux
    assert index != solution


def test_cache_offer(model):
    """Test that forks don't render content when content exists in cache.
    """
    repo = arca.get_repo(model.courses["test-course"].repo, model.courses["test-course"].branch)

    content_key = page_content_cache_key(repo, "beginners/cmdline", "index", None, model.courses["test-course"].vars)

    result = model.courses["test-course"].render_page("beginners/cmdline", "index", None,
                                                      content_key=content_key,
                                                      request_url="/course/test-course/beginners/cmdline/")

    assert result["content"] is None

    # Also test that if provided a key which is gonna be rejected,
    # content is rendered

    result = model.courses["test-course"].render_page("beginners/cmdline", "index", None,
                                                      content_key=content_key + "asdfasdf",
                                                      request_url="/course/test-course/beginners/cmdline/")

    assert result["content"] is not None


def test_courses_page(mocker, client: FlaskClient):
    """Test how /courses/ page behaves when a fork isn't returning course info
    """
    mocker.patch("naucse.utils.views.raise_errors_from_forks", lambda: True)

    # There's a problem in one of the branches, so it should raise an error
    # if the conditions for raising are True
    with pytest.raises(BuildError):
        client.get("/courses/")

    # ... unless problems are silenced
    mocker.patch("naucse.utils.views.raise_errors_from_forks", lambda: False)
    response = client.get("/courses/")
    assert b"Broken course title" not in response.data

    # ... but working forks are still present
    assert b"Course title" in response.data


def test_courses_page_ignore_forks(mocker, client: FlaskClient):
    """Test ignoring forks in courses page
    """
    mocker.patch("naucse.utils.views.forks_enabled", lambda: False)
    mocker.patch("naucse.utils.views.raise_errors_from_forks", lambda: True)

    response = client.get("/courses/")
    assert b"Broken course title" not in response.data
    assert b"Course title" not in response.data


def test_runs_page(mocker, client: FlaskClient):
    """Test how /runs/ page behaves when a fork isn't returning course info
    """
    mocker.patch("naucse.utils.views.forks_enabled", lambda: True)
    mocker.patch("naucse.utils.views.raise_errors_from_forks", lambda: True)

    # There's a problem in one of the branches, so it should raise an error
    # if the conditions for raising are True
    with pytest.raises(BuildError):
        client.get("/runs/all/")

    # unless problems are silenced
    mocker.patch("naucse.utils.views.raise_errors_from_forks", lambda: False)
    response = client.get("/runs/")
    assert b"Broken run title" not in response.data

    # but working forks are still present
    assert b"Run title" in response.data


def test_runs_page_ignore_forks(mocker, client: FlaskClient):
    """Test ignoring forks in runs page
    """
    mocker.patch("naucse.utils.views.forks_enabled", lambda: False)
    mocker.patch("naucse.utils.views.raise_errors_from_forks", lambda: True)

    response = client.get("/runs/all/")

    assert b"Broken run title" not in response.data
    assert b"Run title" not in response.data


@pytest.mark.parametrize("url", [
    "/course/test-course/",
    "/course/test-course/sessions/first-session/",
    "/course/test-course/sessions/first-session/back/",
    "/course/test-course/beginners/cmdline/",
    "/course/test-course/beginners/cmdline/index/solutions/0/",
    "/course/test-course/beginners/install/linux/",
    "/2018/test-run/",
    "/2018/test-run/calendar/",
])
def test_working_pages(url, client: FlaskClient):
    """Test the rendering of the pages is working and not returning a warning.
    """
    response = client.get(url)
    assert b"alert alert-danger" not in response.data


@pytest.mark.parametrize("url", [
    "/course/test-broken-course/",
    "/course/test-broken-course/sessions/first-session/",
    "/course/test-broken-course/sessions/first-session/back/",
    "/course/test-broken-course/beginners/cmdline/",
    "/course/test-broken-course/beginners/cmdline/index/solutions/0/",
    "/course/test-broken-course/beginners/install/linux/",
    "/2018/test-broken-run/",
    "/2018/test-broken-run/calendar/",
])
def test_failing_pages(url, client: FlaskClient):
    """Test that a failing page renders as a page with an error message.
    """
    response = client.get(url)
    assert b"alert alert-danger" in response.data


def test_get_footer_links(model):
    course = model.courses["test-course"]

    # test first lesson of first session
    prev_link, session_link, next_link = course.get_footer_links("beginners/cmdline", "index")

    assert prev_link is None

    assert isinstance(session_link, dict)
    assert session_link["title"] == "First session"
    assert session_link["url"] == "/course/test-course/sessions/first-session/"

    assert isinstance(next_link, dict)
    # titles are dependent on lesson content, let's just check they're there
    assert len(next_link["title"])
    assert next_link["url"] == "/course/test-course/beginners/install/"

    # test last lesson of a session
    prev_link, session_link, next_link = course.get_footer_links("beginners/install", "index")

    assert isinstance(prev_link, dict)
    # titles are dependent on lesson content, let's just check they're there
    assert len(prev_link["title"])
    assert prev_link["url"] == "/course/test-course/beginners/cmdline/"

    assert isinstance(session_link, dict)
    assert session_link["title"] == "First session"
    assert session_link["url"] == "/course/test-course/sessions/first-session/"

    assert isinstance(next_link, dict)
    assert next_link["title"] == "Závěr lekce"
    assert next_link["url"] == "/course/test-course/sessions/first-session/back/"

    # test first lesson of a session with a previous session
    prev_link, session_link, next_link = course.get_footer_links("beginners/first-steps", "index")

    assert prev_link is None

    assert isinstance(session_link, dict)
    assert session_link["title"] == "Second session"
    assert session_link["url"] == "/course/test-course/sessions/second-session/"

    assert isinstance(next_link, dict)
    # titles are dependent on lesson content, let's just check they're there
    assert len(next_link["title"])
    assert next_link["url"] == "/course/test-course/beginners/install-editor/"

    # test nonsense lesson

    with pytest.raises(BuildError):
        course.get_footer_links("custom/non-existing", "index")

    # test nonsense page

    with pytest.raises(BuildError):
        course.get_footer_links("beginners/cmdline", "some-subpage")
