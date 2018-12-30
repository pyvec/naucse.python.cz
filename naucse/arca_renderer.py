from pathlib import Path
import shutil
import re

from arca import Task

import naucse_render


NAUCSE_URL_RE = re.compile(
    '^https://github.com/[^/]+/naucse\.python\.cz(\.git)?$'
)

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

        if NAUCSE_URL_RE.match(url):
            # HACK: Forks of naucse.python.cz don't have a mechanism to
            # get structured data (e.g. titles of lessons).
            # Inject our "naucse_render" into them, and hope for the best
            # XXX: This would be better done by installing naucse_render
            # from PyPI (when it's there).

            hack_path = self.worktree_path / 'naucse_render'
            try:
                shutil.copytree(Path(naucse_render.__file__).parent, hack_path)
            except FileExistsError:
                pass

    def get_course(self, slug, *, version, path):
        task = Task(
            entry_point="naucse_render:get_course",
            args=[slug],
            kwargs={'version': version, 'path': '.'},
        )
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
        info = self.arca.run(self.url, self.branch, task).output

        return info
