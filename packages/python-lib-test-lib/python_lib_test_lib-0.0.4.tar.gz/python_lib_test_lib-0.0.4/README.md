# python-lib-test-lib

[![PyPI](https://img.shields.io/pypi/v/python-lib-test-lib.svg)](https://pypi.org/project/python-lib-test-lib/)
[![Tests](https://github.com/msleigh/python-lib-test-lib/actions/workflows/test.yml/badge.svg)](https://github.com/msleigh/python-lib-test-lib/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/msleigh/python-lib-test-lib?include_prereleases&label=changelog)](https://github.com/msleigh/python-lib-test-lib/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/msleigh/python-lib-test-lib/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

A test library to test the [python-lib](https://github.com/msleigh/python-lib)
Cookiecutter template.

---

## Requirements

Python Lib Test Lib requires Python 3.7+. It is tested on Linux and macOS.

## Installation

Install this library using `pip`:

```bash
pip install python-lib-test-lib
```

## Configuration

Configuration instructions go here.

## Usage

Usage instructions go here.

## Development

To contribute to this library, first checkout the code. Then create a new
virtual environment:

```bash
cd python-lib-test-lib
python -m venv .venv
source .venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install -e '.[test]'
```

To run the tests:

```bash
pytest
```
