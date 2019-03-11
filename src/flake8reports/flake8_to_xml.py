from flake8.formatting.base import BaseFormatter


class Flake8xml(BaseFormatter):

    def format(self, error):
        return error