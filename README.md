# datasette-rure

[![PyPI](https://img.shields.io/pypi/v/datasette-rure.svg)](https://pypi.org/project/datasette-rure/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-rure.svg?style=svg)](https://circleci.com/gh/simonw/datasette-rure)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-rure/blob/master/LICENSE)

Datasette plugin that adds a custom SQL function for executing matches using the Rust regular expression engine

Install this plugin in the same environment as Datasette to enable the `regexp()` SQL function.

    $ pip install datasette-rure

Uses https://github.com/davidblewett/rure-python
