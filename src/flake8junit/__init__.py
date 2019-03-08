
__all__ = ['__version__', '__author__','Flake8JUnit']
from flake8junit.version import __version__, __author__
from flake8.formatting.base import BaseFormatter
from xml.sax.saxutils import escape


class Flake8JUnit(BaseFormatter):
    """Flake8's error text to JUnit XML converter."""
    def _is_error(self, code):
        return len(code) > 0 and code[0] in ('e', 'E')

    def beginning(self, filename):
        super(Flake8JUnit, self).beginning(filename)
        self.write('    <testsuite name="{0}">'.format(filename), None)

    def finished(self, filename):
        self.write('    </testsuite>', None)
        super(Flake8JUnit, self).finished(filename)

    def start(self):
        super(Flake8JUnit, self).start()
        self.write('<?xml version="1.0" encoding="UTF-8"?>', None)
        self.write('<testsuites>', None)

    def handle(self, error):
        line = self.format(error)
        self.write(line, None)

    def format(self, error):
        message = "{0}:{1}:{2} {3} {4}".format(
            escape(error.filename),
            escape(error.line_number),
            escape(error.column_number),
            escape(error.code),
            escape(error.text)
        )
        return '''
        <testcase classname="flake8" name="{0}">
            <failure message="{1}" type="{2}">
{3}
            </failure>
        </testcase>'''.format(
                escape(error.code),
                message,
                'ERROR' if self._is_error(error.code) else 'WARNING',
                escape(self.show_source(error)) if self.options.show_source else ''
            )

    def stop(self):
        self.write('</testsuites>', None)
        super(Flake8JUnit, self).stop()
