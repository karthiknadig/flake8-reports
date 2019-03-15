import inspect
import pytest
import types

@pytest.fixture
def testfile(request, tmpdir):
    def factory(source):
        assert isinstance(source, types.FunctionType)
        name = source.__name__
        source, _ = inspect.getsourcelines(source)

        # First, find the "def" line.
        def_lineno = 0
        for line in source:
            line = line.strip()
            if line.startswith('def') and line.endswith(':'):
                break
            def_lineno += 1
        else:
            raise ValueError('Failed to locate function header.')

        # Remove everything up to and including "def".
        source = source[def_lineno + 1:]
        assert source

        line = source[0]
        indent = len(line) - len(line.lstrip())
        source = [line[indent:] if line.strip() else '\n' for line in source]

        # Write it to file.
        source = ''.join(source)
        tmpfile = tmpdir.join(name + '.py')
        assert not tmpfile.check()
        tmpfile.write(source)
        return tmpfile.strpath

    return factory


@pytest.fixture(
    name='fmt',
    params=['junit', 'xml', 'json', 'csv', 'tsv', 'ssv']
)
def _fmt(request):
    return request.param