from datasette_rure import prepare_connection
import sqlite3
import pytest
import json


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
def test_rure(pattern, input, expected):
    conn = sqlite3.connect(":memory:")
    prepare_connection(conn)
    args = {"pattern": pattern, "input": input}
    sql = "select regexp(:pattern, :input)"
    result = conn.execute(sql, args).fetchone()[0]
    assert expected == result
    # Try the alternative syntax
    sql2 = "select :input REGEXP :pattern"
    result2 = conn.execute(sql2, args).fetchone()[0]
    assert expected == result2
