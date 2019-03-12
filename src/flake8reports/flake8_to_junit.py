import sys

from flake8.formatting.base import BaseFormatter
from xml.etree import ElementTree as ET


class Flake8junit(BaseFormatter):
    """Flake8's error text to JUnit XML converter."""

    def _is_error(self, code):
        return len(code) > 0 and code[0] in ('e', 'E')

    def start(self):
        super(Flake8junit, self).start()
        self._root = ET.Element('testsuite')
        self._root.attrib['name'] = 'flake8'

    def handle(self, error):
        if error.code is not None:
            testcase = ET.SubElement(self._root, 'testcase')
            testcase.attrib['classname'] = 'flake8.%s' % error.code
            testcase.attrib['name'] = error.filename
            testcase.attrib['line'] = '%d' % error.line_number

            failure = ET.SubElement(testcase, 'failure')
            failure.attrib['message'] = "{0}:{1}:{2} {3} {4}".format(
                error.filename,
                error.line_number,
                error.column_number,
                error.code,
                error.text
            )
            failure.attrib['type'] = 'ERROR' if self._is_error(error.code) else 'WARNING'

            if self.options.show_source and error.physical_line is not None:
                failure.text = super(Flake8junit, self).show_source(error)

    def show_statistics(self, statistics):
        for error_code in statistics.error_codes():
            testcase = ET.SubElement(self._root, 'testcase')
            testcase.attrib['classname'] = 'flake8.statistics'
            testcase.attrib['name'] = 'flake8.%s' % error_code

            stats_for_error_code = statistics.statistics_for(error_code)
            statistic = next(stats_for_error_code)
            count = statistic.count
            count += sum(stat.count for stat in stats_for_error_code)
            text = "{count:<5} {error_code} {message}".format(
                count=count,
                error_code=error_code,
                message=statistic.message,
            )
            testcase.attrib['code'] = error_code
            testcase.attrib['count'] = "{count}".format(count=count)
            testcase.attrib['message'] = "{message}".format(message=statistic.message)

            systemout = ET.SubElement(testcase, 'system-out')
            systemout.text = text

    def show_benchmarks(self, benchmarks):
        for benchmark, value in benchmarks:
            testcase = ET.SubElement(self._root, 'testcase')
            testcase.attrib['classname'] = 'flake8.benchmarks'
            testcase.attrib['name'] = benchmark

            if isinstance(value, int):
                text = "{value:<10} {benchmark}".format(benchmark=benchmark, value=value)
            else:
                text = "{value:<10.3} {benchmark}".format(benchmark=benchmark, value=value)

            testcase.attrib['value'] = "{value}".format(value=value)
            systemout = ET.SubElement(testcase, 'system-out')
            systemout.text = text

    def format(self, error):
        return str(error)

    def stop(self):
        self.write('<?xml version="1.0" encoding="utf-8"?>', None)
        res = ET.tostring(self._root, encoding='utf-8')
        if isinstance(res, bytes):
            res = res.decode('utf-8')
        self.write(res, None)
        super(Flake8junit, self).stop()
