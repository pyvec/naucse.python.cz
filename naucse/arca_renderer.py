from pathlib import Path
import contextlib
import shutil
import re

from arca import Task

import naucse_render


NAUCSE_URL_RE = re.compile(
    r'^https://github.com/[^/]+/naucse\.python\.cz(\.git)?$'
)


class RemoteRepoError(Exception):
    """Raised when an Arca call fails and provides info about remote repo"""


class Renderer:
    """Render courses from a remote repository using Arca

    Renderer objects have the same API as the `naucse_render` module.
    """
    def __init__(self, arca, url, branch):
        self.arca = arca
        self.url = url
        self.branch = branch

        readme_path = arca.static_filename(url, branch, 'README.md')
        self.worktree_path = Path(readme_path).parent

    @contextlib.contextmanager
    def wrap_errors(self, method, arg):
        """In case of error, provide extra information about method and repo
        """
        try:
            yield
        except Exception as e:
            raise RemoteRepoError(
                f'Error in {method}({arg!r}), '
                + f'repo {self.url!r}, branch {self.branch!r}'
            ) from e

    def get_course(self, slug, *, version, path):
        task = Task(
            entry_point="naucse_render:get_course",
            args=[slug],
            kwargs={'version': version, 'path': '.'},
        )
        with self.wrap_errors('get_course', slug):
            info = self.arca.run(self.url, self.branch, task).output

        return info

    def get_lessons(self, lesson_slugs, *, vars, path):
        # Default timeout is 5s; multiply this by the no. of requested lessons
        timeout = 5 * len(lesson_slugs)
        task = Task(
            entry_point="naucse_render:get_lessons",
            args=[sorted(lesson_slugs)],
            kwargs={'vars': vars, 'path': '.'},
            timeout=timeout,
        )
        with self.wrap_errors('get_lessons', lesson_slugs):
            info = self.arca.run(self.url, self.branch, task).output

        return info
