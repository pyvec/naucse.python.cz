from pathlib import Path, PosixPath

import pytest

from naucse import edit_info

from test_naucse.conftest import fixture_path


@pytest.mark.parametrize('path', ('.', 'a/b/c', './a/./b'))
def test_relative_path_ok(path):
    assert edit_info.relative_path(path).parts == Path(path).parts


@pytest.mark.parametrize('path', (
    '/',
    '/abc/',
    '../',

    # Technically OK, but disallowing is easier to implement:
    'a/../b',
))
def test_relative_path_fail(path):
    with pytest.raises(ValueError):
        assert edit_info.relative_path('/')


def check_edit_info(repo_info, edit_info):
    """Check that edit_info corresponds to repo_info"""
    assert edit_info.page_name == repo_info.page_name
    assert edit_info.icon == repo_info.icon


REPOINFO_FIXTURES = {
    'none': {
        'get_repo_info': lambda: edit_info.NoRepoInfo(),
        'name': None,
        'icon': None,
        'urls': {'.': None, 'a/b': None},
    },
    'local': {
        'get_repo_info': lambda: edit_info.LocalRepoInfo('/srv/test'),
        'name': None,
        'icon': None,
        'urls': {
            '.': 'file:///srv/test',
            'a/b': 'file:///srv/test/a/b',
        },
    },
    'github_master': {
        'get_repo_info': lambda: edit_info.GithubRepoInfo(
            'encukou', 'empty-repo', 'master'
        ),
        'name': 'GitHubu',
        'icon': 'github',
        'urls': {
            '.': 'https://github.com/encukou/empty-repo',
            'a/b': 'https://github.com/encukou/empty-repo/blob/master/a/b',
        },
    },
    'github_branch': {
        'get_repo_info': lambda: edit_info.GithubRepoInfo(
            'encukou', 'empty-repo', 'somebranch'
        ),
        'name': 'GitHubu',
        'icon': 'github',
        'urls': {
            '.': 'https://github.com/encukou/empty-repo/blob/somebranch/',
            'a/b': 'https://github.com/encukou/empty-repo/blob/somebranch/a/b',
        },
    },
}


@pytest.mark.parametrize('kind', REPOINFO_FIXTURES)
def test_concrete_repo_info(kind):
    repo_info = REPOINFO_FIXTURES[kind]['get_repo_info']()
    assert repo_info.page_name == REPOINFO_FIXTURES[kind]['name']
    assert repo_info.icon == REPOINFO_FIXTURES[kind]['icon']


@pytest.mark.parametrize('kind', REPOINFO_FIXTURES)
@pytest.mark.parametrize('path', REPOINFO_FIXTURES['none']['urls'])
def test_concrete_edit_repo_info(kind, path):
    repo_info = REPOINFO_FIXTURES[kind]['get_repo_info']()
    ei = repo_info.get_edit_info(path)
    assert ei.page_name == REPOINFO_FIXTURES[kind]['name']
    assert ei.icon == REPOINFO_FIXTURES[kind]['icon']
    assert ei.url == REPOINFO_FIXTURES[kind]['urls'][path]


@pytest.mark.parametrize('url', (
    'https://github.com/encukou/empty-repo',
    'git@github.com:encukou/empty-repo',
))
def test_get_repo_info_gh(url):
    repo_info = edit_info.get_repo_info(url, 'master')
    ei = repo_info.get_edit_info('.')
    assert ei.icon == 'github'
    assert ei.url == 'https://github.com/encukou/empty-repo'


@pytest.mark.parametrize('url', (
    'https://some-bazaar-hosting.test/bizarre/naucse-bzr',
))
def test_get_repo_info_unknown(url):
    repo_info = edit_info.get_repo_info(url, 'trunk')
    ei = repo_info.get_edit_info('.')
    assert ei.icon == None
    assert ei.url == None


def test_get_local_repo_info(monkeypatch):
    monkeypatch.delenv('NAUCSE_MAIN_REPO_URL', raising=False)
    repo_info = edit_info.get_local_repo_info(fixture_path)
    ei = repo_info.get_edit_info('.')
    assert ei.icon == None
    assert ei.url == fixture_path.as_uri()


def test_get_local_repo_info_overridden(monkeypatch):
    url = 'https://github.com/encukou/empty-repo'
    monkeypatch.setenv('NAUCSE_MAIN_REPO_URL', url)
    monkeypatch.delenv('NAUCSE_MAIN_REPO_BRANCH', raising=False)
    repo_info = edit_info.get_local_repo_info(fixture_path)
    ei = repo_info.get_edit_info('.')
    assert ei.icon == 'github'
    assert ei.url == url


def test_get_local_repo_info_overridden_branch(monkeypatch):
    url = 'https://github.com/encukou/empty-repo'
    monkeypatch.setenv('NAUCSE_MAIN_REPO_URL', url)
    monkeypatch.setenv('NAUCSE_MAIN_REPO_BRANCH', 'somebranch')
    repo_info = edit_info.get_local_repo_info(fixture_path)
    ei = repo_info.get_edit_info('.')
    assert ei.icon == 'github'
    assert ei.url == 'https://github.com/encukou/empty-repo/blob/somebranch/'
