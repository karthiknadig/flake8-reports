# flake8reports


|     |   |
|-----|---|
|License |[![GitHub](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/Microsoft/ptvsd/master/LICENSE)|
|Info |[![PyPI](https://img.shields.io/pypi/v/flake8reports.svg)](https://pypi.org/project/flake8reports/) [![PyPI](https://img.shields.io/pypi/pyversions/flake8reports.svg)](https://pypi.org/project/flake8reports/)|
|Tests|[![Build Status](https://dev.azure.com/c0d3r/flake8reports/_apis/build/status/flake8reports-yaml?branchName=master)](https://dev.azure.com/c0d3r/flake8reports/_build/latest?definitionId=1&branchName=master) [![PyPI](https://img.shields.io/azure-devops/coverage/c0d3r/flake8reports/1.svg)](https://pypi.org/project/flake8reports/)|

`flake8reports` is a formatting plugin for `flake8`linter.

### Installtion
```console
python -m pip install --pre flake8reports
```

### Usage
Currently supports following formats: xml, json, csv, junit.
```console
flake8 --format=junit .
```
