from flake8.formatting.base import BaseFormatter


class Flake8xsv(BaseFormatter):
    def __init__(self, options):
        self._separator = ','
        super(Flake8xsv, self).__init__()

    def format(self, error):
        return error

class Flake8csv(BaseFormatter):
    def after_init(self):
        self._separator = ','

    def format(self, error):
        return error

class Flake8tsv(BaseFormatter):
    def after_init(self):
        self._separator = '\t'

    def format(self, error):
        return error

class Flake8ssv(BaseFormatter):
    def after_init(self):
        self._separator = ';'

    def format(self, error):
        return error
