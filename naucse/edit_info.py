"""Utilities for the "Edit this page in GitHub" links in footers

In models.py, Each Course (and any other model that's loaded from a different
repository than its parent) has a `repo_info` representing
the *repository* it is hosted at.
Each model then has `edit_info`, which describes where to edit the data for
a particular page.

This is made a bit complicated by the principle that *data doesn't "know" its
container*. The input API doesn't say "this repo is from GitHub", but only
reports relative paths to the repo root.
It's then all assembled on the naucse side.
The list of hosting provider icons & names is at naucse.
"""

import re
import os
from collections import namedtuple
from pathlib import Path
from urllib.parse import urljoin

from git import Repo

from naucse.logger import logger


def relative_path(path):
    """Convert input to Path; ensure that it's relative and within the repo
    """

    path = Path(path)
    if path.is_absolute():
        raise ValueError(f'absolute path: {path}')
    if '..' in path.parts:
        raise ValueError(f'parent directories not allowed: {path}')
    return path


class RepoInfo:
    """Base class for repository information

    Attributes:

    `page_name` should be in Czech dative case for use on the website
    (na "GitHubu"), or None if unknown.

    `icon` should be the icon slug for from Bytesize icons, or None.
    """
    page_name = None
    icon = None

    def get_edit_info(self, path):
        return EditInfo(self, path)


class NoRepoInfo(RepoInfo):
    """Missing repository information"""

    @classmethod
    def from_match(cls, match, branch):
        return cls()

    def get_edit_url(self, path):
        return None


class GithubRepoInfo(RepoInfo):
    """Repository information for github.com"""

    page_name='GitHubu'
    icon='github'

    def __init__(self, org, repo, branch):
        self.base_url = f"https://github.com/{org}/{repo}"
        self.branch = branch

    @classmethod
    def from_match(cls, match, branch):
        return cls(match['org'], match['repo'], branch)

    def get_edit_url(self, path):
        if self.branch == 'master' and str(path) in ('', '.'):
            return self.base_url
        else:
            path = relative_path(path)
            return urljoin(f'{self.base_url}/blob/{self.branch}/', str(path))


class LocalRepoInfo(RepoInfo):
    """Repository information for the local filesystem"""

    def __init__(self, base_path):
        self.base_path = Path(base_path)

    def get_edit_url(self, path):
        path = self.base_path / relative_path(path)
        return path.resolve().as_uri()


class EditInfo:
    """Information about a particular file in a repo"""

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
    """Return repository information for a particular repo URL and branch"""

    for regex, func in _kinds:
        match = re.fullmatch(regex, repo_url)
        if match:
            return func(match, branch)
    logger.debug(f'get_edit_info: repo not matched: {repo_url}')


def get_local_repo_info(path='.'):
    """Return repository information repository for the local filesystem.

    Naucse code doesn't "know" where it's hosted (or cloned from), so this
    information needs to be passed in through NAUCSE_MAIN_REPO_URL and
    NAUCSE_MAIN_REPO_BRANCH.
    If it's not, we display file:// links.
    """
    path = Path(path)

    # Otherwise, fake it!
    assumed_url = os.environ.get('NAUCSE_MAIN_REPO_URL')
    if assumed_url:
        return get_repo_info(
            assumed_url,
            os.environ.get('NAUCSE_MAIN_REPO_BRANCH', 'master'),
        )

    return LocalRepoInfo(path)
