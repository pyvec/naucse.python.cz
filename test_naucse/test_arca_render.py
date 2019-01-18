import subprocess
import textwrap
import logging
import shutil
import json
import os

import pytest
from arca import Arca

from naucse import models
from naucse.arca_renderer import RemoteRepoError

from test_naucse.conftest import fixture_path, make_model, get_local_repo_info
from test_naucse.conftest import assert_yaml_dump


def run(args, *, cwd, check=True, env=None, **kwargs):
    """Like subprocess.run, with logging and different signature/defaults

    - `cwd` (current directory) must be given explicitly
    - `check` (raise error on non-zero exit code) is True by default
    - The environment is set up to (attempt to) isolate Git configuration
    """
    if env is None:
        env = os.environ
    env = dict(env)
    env.setdefault('HOME', str(cwd))
    env.setdefault('XDG_CONFIG_HOME', str(cwd))
    env.setdefault('GIT_CONFIG_NOSYSTEM', '1')
    print('Run:', args)
    return subprocess.run(args, check=check, cwd=cwd, **kwargs)


@pytest.fixture(scope='session')
def git_command():
    """Return the command to execute Git. Skip test if Git is unavailable."""
    cmd = shutil.which('git')
    if cmd is None:
        raise pytest.skip('Git command not found')
    return cmd


@pytest.fixture
def content_repo(tmp_path, git_command):
    """Return path to a fully set-up Git repo with test_content

    The repo is populated with a copy of the "fixtures/test_content" directory.
    """
    repo_path = tmp_path / 'repo'
    shutil.copytree(fixture_path / 'test_content', repo_path)
    run([git_command, 'init'], cwd=repo_path)
    run([git_command, 'config', 'user.name', 'Test User'], cwd=repo_path)
    run([git_command, 'config', 'user.email', 'nobody@test'], cwd=repo_path)
    run([git_command, 'add', '.'], cwd=repo_path)
    run([git_command, 'commit', '-m', 'Initial commit'], cwd=repo_path)
    return repo_path


@pytest.fixture
def arca_model(tmp_path, content_repo):
    """Return a model that loads remote content using Arca"""
    model = make_model(
        arca=Arca(settings={
            "ARCA_BACKEND": "arca.backend.VenvBackend",
            "ARCA_BACKEND_VERBOSITY": 2,
            "ARCA_BASE_DIR": str(tmp_path / '.arca'),
        }),

        # We only trust "master" branches
        trusted_repo_patterns=('*#master',),
    )
    return model


def test_valid_fork(arca_model, content_repo):
    """Valid data can be loaded from a Git repository"""
    course = models.Course.load_remote(
        'courses/normal-course', parent=arca_model,
        link_info={'repo': content_repo.as_uri()},
    )
    arca_model.add_course(course)
    assert_yaml_dump(models.dump(course), 'normal-course.yaml')


def test_yaml_error(arca_model, content_repo, git_command):
    """Invalid YAML raises error with indication of repo, file, line number"""
    yaml_path = content_repo / 'courses/normal-course/info.yml'
    yaml_path.write_text(textwrap.dedent("""
        good: yaml
        *bad_YAML*
    """))

    run([git_command, 'commit', '-a', '-m', 'Break YAML'], cwd=content_repo)

    with pytest.raises(RemoteRepoError):
        try:
            course = models.Course.load_remote(
                'courses/normal-course', parent=arca_model,
                link_info={'repo': content_repo.as_uri()},
            )
        except RemoteRepoError as e:
            # Method, argument, repo is in the RemoteRepoError wrapper
            assert "get_course('courses/normal-course')" in str(e)
            assert "repo 'file://" in str(e)
            assert "branch 'master'" in str(e)

            # File & line info is in Arca's BuildError, the __cause__
            file_line_msg = 'courses/normal-course/info.yml", line 3, column '
            assert file_line_msg in str(e.__cause__)

            # Re-raise to let pytest.raise also validate the error
            raise


def test_lesson_error(arca_model, content_repo, git_command):
    """Bad lesson YAML raises error with indication of repo, file, line no."""
    yaml_path = content_repo / 'courses/bad-course/info.yml'
    yaml_path.parent.mkdir()
    yaml_path.write_text(textwrap.dedent("""
        title: A course with a bad lesson

        sessions:
        - title: A normal session
          slug: normal-session
          materials:
          - lesson_slug: bad/bad
        """))

    lesson_path = content_repo / 'lessons/bad/bad/info.yml'
    lesson_path.parent.mkdir(parents=True)
    lesson_path.write_text(textwrap.dedent("""
        title: An incomplete lesson
    """))

    run([git_command, 'add', '.'], cwd=content_repo)
    run([git_command, 'commit', '-a', '-mAdd bad course'], cwd=content_repo)

    course = models.Course.load_remote(
        'courses/bad-course', parent=arca_model,
        link_info={'repo': content_repo.as_uri()},
    )

    with pytest.raises(RemoteRepoError):
        try:
            course.freeze()
        except RemoteRepoError as e:
            assert "get_lessons({'bad/bad'})" in str(e)
            assert "repo 'file://" in str(e)
            assert "branch 'master'" in str(e)

            # Re-raise to let pytest.raise also validate the error
            raise


def test_removed_data(arca_model, content_repo, git_command):
    """Remove all data; check failing on FileNotFoundError"""
    yaml_path = content_repo / 'courses/normal-course/info.yml'
    run(
        [git_command, 'rm', '-r', 'courses', 'runs', 'lessons'],
        cwd=content_repo,
    )
    run([git_command, 'commit', '-a', '-m', 'Remove all data'], cwd=content_repo)

    with pytest.raises(RemoteRepoError):
        try:
            course = models.Course.load_remote(
                'courses/normal-course', parent=arca_model,
                link_info={'repo': content_repo.as_uri()},
            )
        except RemoteRepoError as e:
            assert 'Task failed' in str(e.__cause__)
            assert 'FileNotFoundError' in str(e.__cause__)
            assert 'courses/normal-course/info.yml' in str(e.__cause__)

            # Re-raise to let pytest.raise also validate the error
            raise


LINK_INFO = {
    'courses/normal-course': {
        'path': 'courses/normal-course',
        'expected_file': 'normal-course.yaml',
    },
    '2000/run-with-times': {
        'path': 'runs/2000/run-with-times',
        'expected_file': 'run-with-times.yaml',
    },
}

def make_data_with_fork_link(tmp_path, course_path, link_content):
    """Make <tmp_path>/data a naucse data directory with a fork link

    The link is at data/<course_path>/link.yml and has the given text content.
    """
    link_yml_path = tmp_path / f'data/{course_path}/link.yml'
    link_yml_path.parent.mkdir(parents=True)
    link_yml_path.write_text(link_content)

    # `data/lessons` needs to exist for `data` to be a naucse data directory
    tmp_path.joinpath('data/lessons').mkdir()


@pytest.mark.parametrize('slug', LINK_INFO)
def test_fork_link(arca_model, content_repo, tmp_path, slug):
    """Test data is loaded via link.yml pointing to a repository"""

    link_info = {'repo': content_repo.as_uri(), 'branch': 'master'}
    make_data_with_fork_link(
        tmp_path, LINK_INFO[slug]["path"], json.dumps(link_info),
    )
    arca_model.load_local_courses(tmp_path / 'data')
    course = arca_model.courses[slug]
    assert_yaml_dump(models.dump(course), LINK_INFO[slug]['expected_file'])


def test_bad_fork_link(arca_model, content_repo, tmp_path):
    """Test that bad link.yml errors out"""
    make_data_with_fork_link(tmp_path, 'courses/bad', 'this is not a dict')
    with pytest.raises(TypeError):
        arca_model.load_local_courses(tmp_path / 'data')


def test_untrusted(arca_model, git_command, content_repo, tmp_path, caplog):
    """Test an untrusted repo/branch is not loaded"""
    run([git_command, 'checkout', '-b', 'untrusted'], cwd=content_repo)

    link_info = {'repo': content_repo.as_uri(), 'branch': 'untrusted'}
    make_data_with_fork_link(
        tmp_path, 'courses/normal-course', json.dumps(link_info),
    )
    arca_model.load_local_courses(tmp_path / 'data')

    with caplog.at_level(logging.DEBUG):
        assert 'courses/normal-course' not in arca_model.courses

    print(caplog.records)
    records = [r for r in caplog.records if r.msg.startswith('Untrusted')]

    assert len(records) == 1
    wanted_message = f'Untrusted repo: {content_repo.as_uri()}#untrusted'
    assert wanted_message in records[0].msg
