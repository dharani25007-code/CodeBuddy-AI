"""CodeBuddy database layer.

Central place for SQLite <-> PostgreSQL connection handling. It patches
``sqlite3.connect`` globally once (via :func:`install_db`) so that every call
site in the app transparently connects to the right backend:

* Local dev (no ``DATABASE_URL``): a fast, WAL-configured SQLite connection.
* Production / Render (``DATABASE_URL`` set): a pooled PostgreSQL connection.

The old approach had ~113 call sites doing ``sqlite3.connect("codebuddy.db")``
inline; keeping that interface is intentional — callers read like SQLite, but
the backend is decided here, in one place, rather than hand-rolled at every
site. This is the single source of truth for connections, so pool exhaustion /
leak bugs have one home to fix instead of hundreds.
"""

import os
import re
import sqlite3

# Preserve the real connector before we patch sqlite3.connect below.
_sqlite_connect = sqlite3.connect

_pg_pool = None  # PostgreSQL connection pool — initialized on first DB call

# Default DB path, resolved from the app root. Set via install_db().
_DB_DEFAULT_PATH = "codebuddy.db"


def _configure_sqlite_connection(conn):
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=-32000")
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA foreign_keys=ON")
    except sqlite3.Error:
        pass
    return conn


def _connect_db(database=None, *args, **kwargs):
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        try:
            import psycopg2
            import psycopg2.extras
            import psycopg2.pool

            # -- Persistent connection pool (created once, reused per request) ------
            # Avoids a new TCP+TLS handshake to Neon on every sqlite3.connect() call.
            global _pg_pool
            if _pg_pool is None:
                try:
                    maxconn = int(os.getenv("PG_POOL_MAXCONN", "20"))
                    _pg_pool = psycopg2.pool.ThreadedConnectionPool(
                        minconn=1, maxconn=maxconn,
                        dsn=DATABASE_URL,
                        connect_timeout=10,
                    )
                except Exception as _pe:
                    print(f"[DB] Pool creation failed: {_pe}")
                    _pg_pool = None

            def _translate_sql(sql):
                # Translate '?' to '%s' only when outside single-quoted string literals
                parts = []
                in_quote = False
                i = 0
                n = len(sql)
                while i < n:
                    ch = sql[i]
                    if ch == "'":
                        if in_quote and i + 1 < n and sql[i + 1] == "'":
                            parts.append("''")
                            i += 2
                            continue
                        in_quote = not in_quote
                        parts.append(ch)
                    elif ch == "?" and not in_quote:
                        parts.append("%s")
                    else:
                        parts.append(ch)
                    i += 1
                translated = "".join(parts)
                translated = translated.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
                translated = translated.replace("AUTOINCREMENT", "SERIAL")
                translated = translated.replace("(datetime('now'))", "CURRENT_TIMESTAMP::text")
                translated = translated.replace("datetime('now')", "CURRENT_TIMESTAMP::text")
                return translated

            class PostgresCursorWrapper:
                def __init__(self, cursor):
                    self._cursor = cursor
                    self._lastrowid = None

                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    self.close()

                def execute(self, sql, parameters=None):
                    sql = _translate_sql(sql)

                    # PostgreSQL handle PRAGMA
                    if sql.strip().upper().startswith("PRAGMA"):
                        match = re.search(r"PRAGMA\s+table_info\((.*?)\)", sql, re.IGNORECASE)
                        if match:
                            table_name = match.group(1).strip("'\"").lower()
                            sql = f"SELECT 0 as cid, column_name as name, data_type as type, 0 as notnull, null as dflt_value, 0 as pk FROM information_schema.columns WHERE table_name = '{table_name}'"
                        else:
                            return self

                    is_insert = sql.strip().upper().startswith("INSERT INTO") and "COLLAB_ROOMS" not in sql.upper()
                    if is_insert and "RETURNING" not in sql.upper():
                        sql = sql.rstrip('; \t\n\r') + " RETURNING id"

                    if parameters:
                        self._cursor.execute(sql, parameters)
                    else:
                        self._cursor.execute(sql)

                    if is_insert and "RETURNING" in sql.upper():
                        try:
                            row = self._cursor.fetchone()
                            if row:
                                self._lastrowid = row[0]
                        except Exception:
                            self._lastrowid = None
                    else:
                        self._lastrowid = None

                    return self

                @property
                def lastrowid(self):
                    return self._lastrowid

                def executemany(self, sql, parameters):
                    sql = _translate_sql(sql)
                    self._cursor.executemany(sql, parameters)
                    return self

                def fetchone(self):
                    return self._cursor.fetchone()

                def fetchall(self):
                    return self._cursor.fetchall()

                def __iter__(self):
                    return iter(self._cursor)

                def close(self):
                    self._cursor.close()

            class PostgresConnectionWrapper:
                def __init__(self, conn, pool):
                    self._conn = conn
                    self._pool = pool
                    self.row_factory = None

                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    if exc_type is not None:
                        self.rollback()
                    else:
                        self.commit()
                    self.close()

                def cursor(self):
                    return PostgresCursorWrapper(self._conn.cursor(cursor_factory=psycopg2.extras.DictCursor))

                def execute(self, sql, parameters=None):
                    cur = self.cursor()
                    cur.execute(sql, parameters)
                    return cur

                def executemany(self, sql, parameters):
                    cur = self.cursor()
                    cur.executemany(sql, parameters)
                    return cur

                def commit(self):
                    self._conn.commit()

                def rollback(self):
                    self._conn.rollback()

                def close(self):
                    if self._conn:
                        if self._pool:
                            try:
                                self._conn.rollback()  # reset any open txn
                                self._pool.putconn(self._conn)
                            except Exception:
                                try:
                                    self._pool.putconn(self._conn, close=True)
                                except Exception:
                                    pass
                        else:
                            try:
                                self._conn.close()
                            except Exception:
                                pass
                        self._conn = None

            # Get a connection from the pool, or fall back to direct connect
            if _pg_pool:
                try:
                    pg_conn = _pg_pool.getconn()
                    is_stale = False
                    if pg_conn.closed:
                        is_stale = True
                    else:
                        try:
                            # Ping check to ensure connection is alive
                            with pg_conn.cursor() as cur:
                                cur.execute("SELECT 1")
                        except Exception:
                            is_stale = True

                    if is_stale:
                        try:
                            _pg_pool.putconn(pg_conn, close=True)
                        except Exception:
                            pass
                        pg_conn = psycopg2.connect(DATABASE_URL)
                        return PostgresConnectionWrapper(pg_conn, None)

                    pg_conn.rollback()
                    return PostgresConnectionWrapper(pg_conn, _pg_pool)
                except Exception:
                    pass
            return PostgresConnectionWrapper(psycopg2.connect(DATABASE_URL), None)
        except Exception as _pge:
            print(f"[DB] PostgreSQL connection failed ({_pge}) — falling back to local SQLite")

    if database in (None, "", "codebuddy.db"):
        database = _DB_DEFAULT_PATH
    kwargs.setdefault("timeout", 30)
    return _configure_sqlite_connection(_sqlite_connect(database, *args, **kwargs))


def install_db(default_db_path="codebuddy.db"):
    """Patch ``sqlite3.connect`` globally and set the default DB path.

    Call once during app startup (app.py) with the resolved DB_PATH. Because
    Python resolves ``sqlite3.connect`` at import/call time, this global patch
    transparently routes every ``sqlite3.connect(...)`` call in the process to
    the configured backend.
    """
    global _DB_DEFAULT_PATH
    _DB_DEFAULT_PATH = default_db_path
    sqlite3.connect = _connect_db