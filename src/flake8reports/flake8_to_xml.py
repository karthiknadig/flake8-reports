from flake8.formatting.base import BaseFormatter
from xml.etree import ElementTree as ET


class Flake8xml(BaseFormatter):
    """Flake8's error text to XML converter."""

    def _is_error(self, code):
        return len(code) > 0 and code[0] in ('e', 'E')

    def start(self):
        super(Flake8xml, self).start()
        self._root = ET.Element('report')
        self._reports = ET.SubElement(self._root, 'errors')

    def handle(self, error):
        if error.code is not None:
            name = 'error' if self._is_error(error.code) else 'warning'
            data = ET.SubElement(self._reports, name)
            data.attrib['filename'] = error.filename
            data.attrib['line'] = '%d' % error.line_number
            data.attrib['column'] = '%d' % error.column_number
            data.attrib['code'] = error.code
            data.attrib['message'] = error.text

            if self.options.show_source and error.physical_line is not None:
                data.text = super(Flake8xml, self).show_source(error)

    def show_statistics(self, statistics):
        stats = ET.SubElement(self._root, 'stats')
        for error_code in statistics.error_codes():
            stat = ET.SubElement(stats, 'testcase')

            stats_for_error_code = statistics.statistics_for(error_code)
            statistic = next(stats_for_error_code)
            count = statistic.count
            count += sum(stat.count for stat in stats_for_error_code)

            stat.attrib['name'] = error_code
            stat.attrib['count'] = "{count}".format(count=count)
            stat.attrib['message'] = "{message}".format(message=statistic.message)

    def show_benchmarks(self, benchmarks):
        bmarks = ET.SubElement(self._root, 'benchmarks')
        for benchmark, value in benchmarks:
            bmark = ET.SubElement(bmarks, 'benchmark')
            bmark.attrib['name'] = benchmark
            bmark.attrib['value'] = "{value}".format(value=value)

    def format(self, error):
        return str(error)

    def stop(self):
        self.write('<?xml version="1.0" encoding="utf-8"?>', None)
        res = ET.tostring(self._root, encoding='utf-8')
        if isinstance(res, bytes):
            res = res.decode('utf-8')
        self.write(res, None)
        super(Flake8xml, self).stop()