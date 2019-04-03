# flake8-reports


|     |   |
|-----|---|
|License |[![GitHub](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/karthiknadig/flake8-reports/master/LICENSE)|
|Info |[![PyPI](https://img.shields.io/pypi/v/flake8reports.svg)](https://pypi.org/project/flake8-reports/) [![PyPI](https://img.shields.io/pypi/pyversions/flake8reports.svg)](https://pypi.org/project/flake8-reports/)|
|Tests|[![Build Status](https://dev.azure.com/c0d3r/flake8reports/_apis/build/status/flake8reports-yaml?branchName=master)](https://dev.azure.com/c0d3r/flake8reports/_build/latest?definitionId=1&branchName=master) [![PyPI](https://img.shields.io/azure-devops/coverage/c0d3r/flake8reports/1.svg)](https://pypi.org/project/flake8-reports/)|

`flake8-reports` is a formatting plugin for `flake8`linter.

### Installtion
```console
python -m pip install --pre flake8-reports
```

### Usage
Currently supports following formats: xml, json, csv, junit.
```console
flake8 --format=junit .
```
