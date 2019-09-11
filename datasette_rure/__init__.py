from datasette import hookimpl
import functools
import threading
import json
import rure


@functools.lru_cache(maxsize=128)
def _compiled_regex(threadid, pattern):
    return rure.compile(pattern)


def compiled_regex(pattern):
    return _compiled_regex(threading.get_ident(), pattern)


def none_on_exception(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            return None

    return inner


@none_on_exception
def regexp(pattern, input):
    return 1 if compiled_regex(pattern).search(input) else 0


@none_on_exception
def regexp_match(pattern, input, index=1):
    return compiled_regex(pattern).match(input).group(index)


@none_on_exception
def regexp_matches(pattern, input):
    return json.dumps([m.groupdict() for m in compiled_regex(pattern).finditer(input)])


@hookimpl
def prepare_connection(conn):
    conn.create_function("regexp", 2, regexp)
    conn.create_function("regexp_match", 2, regexp_match)
    conn.create_function("regexp_match", 3, regexp_match)
    conn.create_function("regexp_matches", 2, regexp_matches)
