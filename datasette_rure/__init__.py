from datasette import hookimpl
import rure


def regexp(y, x):
    return 1 if rure.search(y, x) else 0


@hookimpl
def prepare_connection(conn):
    conn.create_function("regexp", 2, regexp)
