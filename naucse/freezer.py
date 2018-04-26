import contextlib
from collections import deque

from flask import current_app
from flask_frozen import UrlForLogger, Freezer

def record_url(url):
    """Logs that `url` should be included in the resulting static site"""
    urls_to_freeze = current_app.config.get('NAUCSE_ABSOLUTE_URLS_TO_FREEZE')
    if urls_to_freeze is not None:
        urls_to_freeze.append(url)


class AllLinksLogger(UrlForLogger):
    """Logs ``url_for`` calls, but yields urls from ``absolute_urls_to_freeze`` as well.
    """

    def __init__(self, app, urls_to_freeze):
        super().__init__(app)
        self.naucse_urls_to_freeze = urls_to_freeze

    def iter_calls(self):
        """Yield all logged urls and links parsed from content.
        """
        # Unfortunately, ``yield from`` cannot be used as the queues are
        # modified on the go.
        while self.logged_calls or self.naucse_urls_to_freeze:
            while self.logged_calls:
                yield self.logged_calls.popleft()
            # Prefer URLs from logged_calls - ideally, cache is populated
            # from the base repository.
            # That means we only yield from urls_to_freeze
            # if there are no logged_calls.
            if self.naucse_urls_to_freeze:
                yield self.naucse_urls_to_freeze.popleft()


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

        urls_to_freeze = deque()

        with app.app_context():
            app.config['NAUCSE_ABSOLUTE_URLS_TO_FREEZE'] = urls_to_freeze

        # override the default url_for_logger with our modified version
        self.url_for_logger = AllLinksLogger(app, urls_to_freeze)
