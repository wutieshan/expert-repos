import sqlite3
import threading
from .base import Proxy, Options


class SQLiteOptions(Options):
    dbpath: str = ":memory:"


class SQLiteProxy(Proxy):
    def __init__(self, options: SQLiteOptions) -> None:
        super().__init__()
        self._mutex = threading.Lock()
        self._conn = None
        self._options = options

    def connect(self):
        super().connect()
        with self._mutex:
            if self._conn is None:
                self._conn = sqlite3.connect(
                    database=self._options.dbpath,
                    check_same_thread=False,
                    detect_types=sqlite3.PARSE_DECLTYPES,
                    autocommit=True,
                )
                self._conn.row_factory = sqlite3.Row

    def close(self):
        super().close()
        with self._mutex:
            if self._conn is not None:
                self._conn.close()
                self._conn = None

    def commit(self):
        super().commit()
        self._conn.commit()

    def execute(self, sqltext: str, params: tuple = None):
        self.connect()
        with self._mutex:
            cursor = self._conn.execute(sqltext, params or ())
            return cursor

    def executescript(self, sqltext: str):
        self.connect()
        with self._mutex:
            cursor = self._conn.executescript(sqltext)
            return cursor
