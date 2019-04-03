import json
from flake8.formatting.base import BaseFormatter


class Flake8json(BaseFormatter):

    def _is_error(self, code):
        return len(code) > 0 and code[0] in ('e', 'E')

    def start(self):
        super(Flake8json, self).start()
        self.errors = []
        self.warnings = []
        self.statistics = []
        self.benchmarks = []

    def handle(self, error):
        if error.code is not None:
            source = None
            if self.options.show_source and error.physical_line is not None:
                source = super(Flake8json, self).show_source(error)
            obj = {
                'filename': error.filename,
                'line': error.line_number,
                'column': error.column_number,
                'code': error.code,
                'message': error.text,
                'source': source
            }
            if self._is_error(error.code):
                self.errors.append(obj)
            else:
                self.warnings.append(obj)

    def show_statistics(self, statistics):
        for error_code in statistics.error_codes():
            stats_for_error_code = statistics.statistics_for(error_code)
            statistic = next(stats_for_error_code)
            count = statistic.count
            count += sum(stat.count for stat in stats_for_error_code)

            self.statistics.append({'code': error_code, 'count': count, 'message': statistic.message})

    def show_benchmarks(self, benchmarks):
        for benchmark, value in benchmarks:
            self.benchmarks.append({'benchmark': benchmark, 'value': value})

    def format(self, error):
        return str(error)

    def stop(self):
        obj = {
            'errors': self.errors,
            'warnings': self.warnings,
            'statistics': self.statistics,
            'benchmarks': self.benchmarks
        }
        self.write(json.dumps(obj), None)
        super(Flake8json, self).stop()
