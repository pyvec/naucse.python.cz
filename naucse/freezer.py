import contextlib
from collections import deque

from flask_frozen import UrlForLogger, Freezer

absolute_urls_to_freeze = deque()

def record_url(url):
    """Logs that `url` should be included in the resulting static site"""
    absolute_urls_to_freeze.append(url)


class AllLinksLogger(UrlForLogger):
    """Logs ``url_for`` calls, but yields urls from ``absolute_urls_to_freeze`` as well.
    """

    def iter_calls(self):
        """Yield all logged urls and links parsed from content.
        """
        # Unfortunately, ``yield from`` cannot be used as the queues are
        # modified on the go.
        while self.logged_calls or absolute_urls_to_freeze:
            if self.logged_calls:
                yield self.logged_calls.popleft()
                # prefer urls from :atrr:`logged_calls` - so, ideally,
                # cache is populated from the base repository
                continue
            if absolute_urls_to_freeze:
                yield absolute_urls_to_freeze.popleft()


@contextlib.contextmanager
def temporary_url_for_logger(app):
    """Context manager which temporary adds a new UrlForLogger to the app.

    The logger is yielded as the context object, so it can be used
    to get logged calls.
    """
    logger = UrlForLogger(app)

    yield logger

    # reverses the following operating from :class:`UrlForLogger`
    # self.app.url_default_functions.setdefault(None, []).insert(0, logger)
    app.url_default_functions[None].pop(0)


class NaucseFreezer(Freezer):

    def __init__(self, app):
        super().__init__(app)

        # override the default url_for_logger with our modified version
        self.url_for_logger = AllLinksLogger(app)
