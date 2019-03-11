import sys

from flake8.formatting.base import BaseFormatter
from xml.etree import ElementTree as ET


class Flake8junit(BaseFormatter):
    """Flake8's error text to JUnit XML converter."""

    def _is_error(self, code):
        return len(code) > 0 and code[0] in ('e', 'E')

    def beginning(self, filename):
        super(Flake8junit, self).beginning(filename)
        assert self._testsuite is None
        self._testsuite = ET.Element('testsuite')
        self._testsuite.attrib['name'] = filename

    def finished(self, filename):
        assert self._testsuite is not None
        if len(list(self._testsuite)) > 0:
            self._root.append(self._testsuite)
        self._testsuite = None
        super(Flake8junit, self).finished(filename)

    def start(self):
        super(Flake8junit, self).start()
        self._root = ET.Element('testsuites')
        self._testsuite = None

    def handle(self, error):
        assert self._testsuite is not None
        if error.code is not None:
            testcase = ET.SubElement(self._testsuite, 'testcase')
            testcase.attrib['classname'] = 'flake8'
            testcase.attrib['name'] = error.filename

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
        testsuite = ET.Element('testsuite')
        testsuite.attrib['name'] = 'statistics'

        for error_code in statistics.error_codes():

            testcase = ET.SubElement(testsuite, 'testcase')
            testcase.attrib['classname'] = 'flake8'
            testcase.attrib['name'] = error_code

            stats_for_error_code = statistics.statistics_for(error_code)
            statistic = next(stats_for_error_code)
            count = statistic.count
            count += sum(stat.count for stat in stats_for_error_code)
            text = "{count:<5} {error_code} {message}".format(
                count=count,
                error_code=error_code,
                message=statistic.message,
            )

            systemout = ET.SubElement(testcase, 'system-out')
            systemout.text = text

        self._root.append(testsuite)

    def show_benchmarks(self, benchmarks):
        testsuite = ET.Element('testsuite')
        testsuite.attrib['name'] = 'benchmarks'

        float_format = "{value:<10.3} {statistic}".format
        int_format = "{value:<10} {statistic}".format

        for statistic, value in benchmarks:

            testcase = ET.SubElement(testsuite, 'testcase')
            testcase.attrib['classname'] = 'flake8'
            testcase.attrib['name'] = statistic

            if isinstance(value, int):
                benchmark = int_format(statistic=statistic, value=value)
            else:
                benchmark = float_format(statistic=statistic, value=value)

            systemout = ET.SubElement(testcase, 'system-out')
            systemout.text = benchmark

        self._root.append(testsuite)

    def format(self, error):
        return str(error)

    def stop(self):
        self.write('<?xml version="1.0" encoding="utf-8"?>', None)
        res = ET.tostring(self._root, encoding='utf-8')
        if isinstance(res, bytes):
            res = res.decode('utf-8')
        self.write(res, None)
        super(Flake8junit, self).stop()
