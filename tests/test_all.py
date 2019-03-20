import os
import pytest
import sys
import subprocess
from xml.etree import ElementTree as ET
from tests.helpers.util import is_int, is_real


def _validate_junit(result, **options):
    show_source = options.get('show_source', False)
    expect_stats = options.get('statistic', False)
    expect_benchmarks = options.get('benchmark', False)
    root = ET.fromstring(result)
    assert root.tag == 'testsuite'
    assert sorted(list(root.attrib.keys())) == ['errors', 'failures', 'name', 'tests', 'time']
    assert root.attrib['name'] == 'flake8'

    testcases = list(root)
    assert int(root.attrib['tests']) == len(testcases)
    assert int(root.attrib['failures']) == len(testcases)
    assert int(root.attrib['errors']) == 0

    statistics = list(t for t in testcases
                      if t.attrib['classname'] == 'flake8.statistics')
    benchmarks = list(t for t in testcases
                      if t.attrib['classname'] == 'flake8.benchmarks')

    testcases = list(t for t in testcases
                     if t.attrib['classname'] not in ('flake8.statistics', 'flake8.benchmarks'))
    for testcase in testcases:
        assert testcase.tag == 'testcase'
        assert testcase.attrib['classname'].startswith('flake8')
        assert is_int(testcase.attrib['line'])
        assert is_int(testcase.attrib['time'])
        assert testcase.attrib['name'] is not None

        children = list(testcase)
        for child in children:
            # <failure message=" text " type="ERROR|WARNING" />
            # <system-out> text </system-out>
            assert child.tag in ('failure', 'system-out')
            if child.tag == 'failure':
                assert child.attrib['type'] in ('ERROR', 'WARNING')
                assert child.attrib['message'] is not None
                if show_source:
                    assert len(child.text) > 0

    if expect_stats:
        assert len(statistics) > 0

    for stat in statistics:
        assert stat.tag == 'testcase'
        assert stat.attrib['classname'] == 'flake8.statistics'
        assert stat.attrib['code'] is not None
        assert is_int(stat.attrib['count'])
        assert stat.attrib['message'] is not None

        children = list(stat)
        assert len(children) == 1
        assert children[0].tag == 'system-out'
        assert len(children[0].text) > 0

    if expect_benchmarks:
        assert len(benchmarks) > 0

    for bmark in benchmarks:
        assert stat.tag == 'testcase'
        assert stat.attrib['classname'] == 'flake8.benchmarks'
        assert stat.attrib['name'] is not None
        value = stat.attrib['value']
        assert value is not None
        assert is_int(value) or is_real(value)

        children = list(stat)
        assert len(children) == 1
        assert children[0].tag == 'system-out'
        assert len(children[0].text) > 0


def _validate_xml(result, **options):
    show_source = options.get('show_source', False)
    expect_stats = options.get('statistic', False)
    expect_benchmarks = options.get('benchmark', False)

    root = ET.fromstring(result)
    assert root.tag == 'report'
    children = list(root)

    errors = list(c for c in children if c.tag == 'errors')
    assert len(errors) == 1
    errors = errors[0]

    for error in errors:
        assert error.tag in ('error', 'warning')
        assert len(error.attrib['filename']) > 0
        assert is_int(error.attrib['line'])
        assert is_int(error.attrib['column'])
        assert error.attrib['code'] is not None
        assert len(error.attrib['message']) > 0

        if show_source:
            assert len(error.text) > 0

    if expect_stats:
        statistics = list(c for c in children if c.tag == 'statistics')
        assert len(statistics) == 1
        statistics = statistics[0]

        for statistic in statistics:
            assert statistic.tag == 'statistic'
            assert len(statistic.attrib['code']) > 0
            assert is_int(statistic.attrib['count'])
            assert len(statistic.attrib['message']) > 0

    if expect_benchmarks:
        benchmarks = list(c for c in children if c.tag == 'statistics')
        assert len(benchmarks) == 1
        benchmarks = benchmarks[0]

        for benchmark in benchmarks:
            assert benchmark.tag == 'benchmark'
            assert len(benchmark.attrib['name']) > 0
            value = benchmark.attrib['value']
            assert is_int(value) or is_real(value)


def _validate_json(result, **options):
    pass


def _validate_csv(result, **options):
    pass


def _validate_tsv(result, **options):
    pass


def _validate_ssv(result, **options):
    pass


_validate = {
    'junit': _validate_junit,
    'xml': _validate_xml,
    'json': _validate_json,
    'csv': _validate_csv,
    'tsv': _validate_tsv,
    'ssv': _validate_ssv,
}


@pytest.mark.timeout(10)
def test_flake8_output(fmt, testfile, tmpdir):
    @testfile
    def code_to_lint():
        a=1

    result_file = '{0}'.format(tmpdir.join('result.txt'))
    args = [sys.executable, '-m', 'flake8', '--format={0}'.format(fmt), '--output-file', result_file]
    cwd = os.path.dirname(code_to_lint)

    process = subprocess.Popen(args, cwd=cwd)
    try:
        process.wait(5)
    except TypeError:
        # Python 2.* wait does not take any arguments.
        process.wait()

    with open(result_file, 'r') as res:
        result = res.read()
        print('RESULT: ' + result)
        _validate[fmt](result)
