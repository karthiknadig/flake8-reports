import os
import pytest
import sys
import subprocess
from xml.etree import ElementTree as ET

def _validate_junit(result, **options):
    root = ET.fromstring(result)
    assert root.tag == 'testsuite'
    assert sorted(list(root.attrib.keys())) == ['errors', 'failures', 'name', 'tests', 'time']
    assert root.attrib['name'] == 'flake8'

    children = list(root)
    assert int(root.attrib['tests']) == len(children)
    assert int(root.attrib['failures']) == len(children)
    assert int(root.attrib['errors']) == 0

def _validate_xml(result, **options):
    pass

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

    result_file = tmpdir.join('result.txt')
    args = [sys.executable, '-m', 'flake8', '--format={0}'.format(fmt), '--output-file={0}'.format(result_file)]
    cwd = os.path.dirname(code_to_lint)
    process = subprocess.Popen(args, cwd=cwd)
    process.wait(5)
    with open(result_file, 'r') as res:
        result = res.read()
        print('RESULT: ' + result)
        _validate[fmt](result)
