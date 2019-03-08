
__all__ = ['__version__', '__author__','Flake8JUnitPlugin']
from flake8junit.version import __version__, __author__
from flake8.formatting.base import BaseFormatter


class Flake8JUnitPlugin(BaseFormatter):
    """Flake8's error text to JUnit XML converter."""

    def format(self, error):
        return error
