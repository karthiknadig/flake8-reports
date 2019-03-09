from flake8.formatting.base import BaseFormatter


class Flake8json(BaseFormatter):

    def format(self, error):
        return error