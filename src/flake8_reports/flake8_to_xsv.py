import csv
from flake8.formatting.base import BaseFormatter
try:
    import StringIO
except ImportError:
    import io as StringIO


class Flake8xsv(BaseFormatter):
    def __init__(self, options):
        self._dialect = 'excel'
        super(Flake8xsv, self).__init__(options)

    def start(self):
        super(Flake8xsv, self).start()
        self.rows = []

    def handle(self, error):
        if error.code is not None:
            row = [error.filename, error.line_number, error.column_number, error.code, error.text]

            if self.options.show_source and error.physical_line is not None:
                row += [super(Flake8xsv, self).show_source(error)]

            self.rows.append(row)

    def show_statistics(self, statistics):
        self.rows.append(['statistics'])
        for error_code in statistics.error_codes():
            stats_for_error_code = statistics.statistics_for(error_code)
            statistic = next(stats_for_error_code)
            count = statistic.count
            count += sum(stat.count for stat in stats_for_error_code)
            self.rows.append([error_code, count, statistic.message])

    def show_benchmarks(self, benchmarks):
        self.rows.append(['benchmarks'])
        for benchmark, value in benchmarks:
            self.rows.append([benchmark, value])

    def format(self, error):
        return str(error)

    def stop(self):
        str_stream = StringIO.StringIO()
        csv_stream = csv.writer(str_stream, dialect=self._dialect)
        csv_stream.writerows(self.rows)
        self.write(str_stream.getvalue(), None)
        super(Flake8xsv, self).stop()


class Flake8csv(Flake8xsv):
    def after_init(self):
        self._dialect = csv.excel


class Flake8tsv(Flake8xsv):
    def after_init(self):
        self._dialect = csv.excel_tab


class Flake8ssv(Flake8xsv):
    def after_init(self):
        csv.register_dialect('semicolon', delimiter=';', quoting=csv.QUOTE_MINIMAL)
        self._dialect = 'semicolon'
