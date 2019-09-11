from datasette import hookimpl
import functools
import json
import rure


def none_on_exception(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            return None

    return inner


@none_on_exception
def regexp(y, x):
    return 1 if rure.search(y, x) else 0


@none_on_exception
def regexp_match(pattern, input, index=1):
    return rure.match(pattern, input).group(index)


@none_on_exception
def regexp_matches(pattern, input):
    return json.dumps([m.groupdict() for m in rure.finditer(pattern, input)])


@hookimpl
def prepare_connection(conn):
    conn.create_function("regexp", 2, regexp)
    conn.create_function("regexp_match", 2, regexp_match)
    conn.create_function("regexp_match", 3, regexp_match)
    conn.create_function("regexp_matches", 2, regexp_matches)
