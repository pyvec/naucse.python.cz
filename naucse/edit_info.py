import re
import os
from collections import namedtuple
from pathlib import Path

from git import Repo

from naucse.logger import logger


class GithubEditInfo:
    page_name='GitHubu'
    icon='github'

    def __init__(self, org, repo, branch, path='/'):
        self.org = org
        self.repo = repo
        self.branch = branch
        self.path = path
        if branch == 'master' and path in ('', '/', '.'):
            self.url = (f"https://github.com/{org}/{repo}")
        else:
            self.url = (f"https://github.com/{org}/{repo}/blob/{branch}/{path}")

    @classmethod
    def from_match(cls, match, branch, path):
        match
        return cls(match['org'], match['repo'], branch, path)

    def get_edit_url(self, path):
        return f"{self.base_url}/{path}"

    def __truediv__(self, path):
        return type(self)(self.org, self.repo, self.branch, self.path + path)


_kinds = [
    ('https://github.com/(?P<org>[^/]+)/(?P<repo>[^/]+?)(.git)?',
         GithubEditInfo.from_match),
    ('git@github.com:(?P<org>[^/]+)/(?P<repo>[^/]+?)(.git)?',
         GithubEditInfo.from_match),
]


def get_edit_info(repo_url, branch, path):
    for regex, func in _kinds:
        match = re.fullmatch(regex, repo_url)
        if match:
            return func(match, branch, path)
    logger.debug(f'get_edit_info: repo not matched: {repo_url}')


def get_local_edit_info(path='.'):
    """Return the slug of the repository based on the current branch.

    Returns the default if not on a branch, the branch doesn't
    have a remote, or the remote url can't be parsed.
    """
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

    repo = Repo(str(path), search_parent_directories=True)

    logger.debug(f'in branch active_branch')

    try:
        active_branch = branch = repo.active_branch
    except TypeError:
        # not in a branch
        logger.debug('get_local_edit_info: Not in a branch')
        return None

    logger.debug(f'in branch {active_branch}')

    try:
        remote_name = active_branch.remote_name
    except ValueError:
        tracking_branch = active_branch.tracking_branch()

        if tracking_branch is None:
            # a branch without a remote
            logger.debug(
                f'get_local_edit_info: No tracking branch for {active_branch}'
            )
            return None

        try:
            remote_name = tracking_branch.remote_name
            branch = tracking_branch.remote_head
        except ValueError:
            # tracking branch without a remote
            logger.debug(
                f'get_local_edit_info: No remote for {tracking_branch}'
            )
            return None

    remote_url = repo.remotes[remote_name].url
    relative_path = str(path.relative_to(repo.working_dir))

    return get_edit_info(remote_url, branch, path=relative_path)
