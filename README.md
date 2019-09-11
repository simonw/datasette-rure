# datasette-rure

[![PyPI](https://img.shields.io/pypi/v/datasette-rure.svg)](https://pypi.org/project/datasette-rure/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-rure.svg?style=svg)](https://circleci.com/gh/simonw/datasette-rure)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-rure/blob/master/LICENSE)

Datasette plugin that adds a custom SQL function for executing matches using the Rust regular expression engine

Install this plugin in the same environment as Datasette to enable the `regexp()` SQL function.

    $ pip install datasette-rure

The plugin is built on top of Uses https://github.com/davidblewett/rure-python

## regexp() to test regular expressions

You can test if a value matches a regular expression like this:

    select regexp('hi.*there', 'hi there')
    -- returns 1
    select regexp('not.*there', 'hi there')
    -- returns 0

You can also use SQLite's custom syntax to run matches:

    select 'hi there' REGEXP 'hi.*there'
    -- returns 1

This means you can select rows based on regular expression matches - for example, to select every article where the title begins with a lower-case letter:

    select * from articles where title REGEXP '^[a-z]'

## regexp_match() to extract groups

You can extract captured subsets of a pattern using `regexp_match()`.

    select regexp_match('.*( and .*)', title) as n from articles where n is not null
    -- Returns the ' and X' component of any matching titles, e.g.
    --     and Recognition
    --     and Transitions Their Place
    -- etc

This will return the first parenthesis match when called with two arguments. You can call it with three arguments to indicate which match you would like to extract:

    select regexp_match('.*(and)(.*)', title, 2) as n from articles where n is not null

The function will return `null` for invalid inputs e.g. a pattern without capture groups.

## regexp_matches() to extract multiple matches at once

The `regexp_matches()` function can be used to extract multiple patterns from a single string. The result is returned as a JSON array, which can then be further processed using SQLite's [JSON functions](https://www.sqlite.org/json1.html).

The first argument is a regular expression with named capture groups. The second argument is the string to be matched.

    select regexp_matches(
        'hello (?P<name>\w+) the (?P<species>\w+)',
        'hello bob the dog, hello maggie the cat, hello tarquin the otter'
    )

This will return a list of JSON objects, each one representing the named captures from the original regular expression:

    [
        {"name": "bob", "species": "dog"},
        {"name": "maggie", "species": "cat"},
        {"name": "tarquin", "species": "otter"}
    ]
