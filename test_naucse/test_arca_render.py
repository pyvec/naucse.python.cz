import subprocess
import textwrap
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
        trusted_repo_patterns=('*',),
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


@pytest.mark.parametrize('slug', LINK_INFO)
def test_fork_link(arca_model, content_repo, tmp_path, slug):
    link_yml_path = tmp_path / f'data/{LINK_INFO[slug]["path"]}/link.yml'
    link_yml_path.parent.mkdir(parents=True)
    with link_yml_path.open('w') as f:
        json.dump({'repo': content_repo.as_uri(), 'branch': 'master'}, f)

    # `data/lessons` needs to exist for `data` to be a naucse data directory
    tmp_path.joinpath('data/lessons').mkdir()

    arca_model.load_local_courses(tmp_path / 'data')

    course = arca_model.courses[slug]
    assert_yaml_dump(models.dump(course), LINK_INFO[slug]['expected_file'])
