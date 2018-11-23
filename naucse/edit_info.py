import re
import os
from collections import namedtuple
from pathlib import Path

from git import Repo

from naucse.logger import logger


class RepoInfo:
    page_name = None
    icon = None

    def get_edit_info(self, path):
        return EditInfo(self, path)


class NoRepoInfo(RepoInfo):
    @classmethod
    def from_match(cls, match, branch):
        return cls()

    def get_edit_url(self, path):
        return path


class GithubRepoInfo(RepoInfo):
    page_name='GitHubu'
    icon='github'

    def __init__(self, org, repo, branch):
        self.base_url = f"https://github.com/{org}/{repo}"
        self.branch = branch

    @classmethod
    def from_match(cls, match, branch):
        return cls(match['org'], match['repo'], branch)

    def get_edit_url(self, path):
        if self.branch == 'master' and path in ('', '/', '.'):
            return self.base_url
        else:
            return f"{self.base_url}/blob/{self.branch}/{path}"


class LocalRepoInfo(RepoInfo):
    def __init__(self, base_path):
        self.base_path = Path(base_path)

    def get_edit_url(self, path):
        return (self.base_path / path).resolve().as_uri()


class EditInfo:
    def __init__(self, repo_info, path):
        self.page_name = repo_info.page_name
        self.icon = repo_info.icon
        self.url = repo_info.get_edit_url(path)


_kinds = [
    ('https://github.com/(?P<org>[^/]+)/(?P<repo>[^/]+?)(.git|/)?',
         GithubRepoInfo.from_match),
    ('git@github.com:(?P<org>[^/]+)/(?P<repo>[^/]+?)(.git|/)?',
         GithubRepoInfo.from_match),
    ('.*', NoRepoInfo.from_match),
]


def get_repo_info(repo_url, branch):
    for regex, func in _kinds:
        match = re.fullmatch(regex, repo_url)
        if match:
            return func(match, branch)
    logger.debug(f'get_edit_info: repo not matched: {repo_url}')


def get_local_repo_info(path='.'):
    """Return the slug of the repository based on the current branch."""
    path = Path(path)

    # Travis CI checks out specific GitHub commit; there isn't an active branch
    if os.environ.get('TRAVIS'):
        repo_slug = os.environ.get('TRAVIS_PULL_REQUEST_SLUG')
        if repo_slug:
            branch = os.environ['TRAVIS_PULL_REQUEST_BRANCH']
        else:
            repo_slug = os.environ['TRAVIS_REPO_SLUG']
            branch = os.environ['TRAVIS_BRANCH']
        if not repo_slug:
            return None
        return GithubEditInfo(*repo_slug.split('/', 1), branch)

    # Otherwise, fake it!
    assumed_url = os.environ.get('NAUCSE_MAIN_REPO_URL')
    if assumed_url:
        return get_repo_info(
            assumed_url,
            os.environ.get('NAUCSE_MAIN_REPO_BRANCH', 'master'),
        )

    return LocalRepoInfo('.')
