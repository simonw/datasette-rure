from datasette_rure import prepare_connection
import sqlite3
import pytest
import json


@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    prepare_connection(conn)
    return conn


@pytest.mark.parametrize(
    "pattern,input,expected",
    (
        ("a", "a", True),
        ("a", "b", False),
        ("do?g", "dog", True),
        ("do?g", "dg", True),
        ("do?g", "dig", False),
    ),
)
def test_regexp(conn, pattern, input, expected):
    args = {"pattern": pattern, "input": input}
    sql = "select regexp(:pattern, :input)"
    result = conn.execute(sql, args).fetchone()[0]
    assert expected == result
    # Try the alternative syntax
    sql2 = "select :input REGEXP :pattern"
    result2 = conn.execute(sql2, args).fetchone()[0]
    assert expected == result2


def test_regexp_match_2_arguments(conn):
    sql = "select regexp_match(?, ?)"
    result = conn.execute(sql, ("hello(.*)dog", "hello there dog")).fetchone()[0]
    assert " there " == result


def test_regexp_match_3_arguments(conn):
    sql = "select regexp_match(?, ?, 2)"
    result = conn.execute(
        sql, ("hello(.*)dog(.*)and", "hello there dog cat and")
    ).fetchone()[0]
    assert " cat " == result


def test_regexp_match_none_on_error(conn):
    sql = "select regexp_match(?, ?)"
    # No capturing parenthesis:
    result = conn.execute(sql, ("hello dog", "hello dog")).fetchone()[0]
    assert result is None
