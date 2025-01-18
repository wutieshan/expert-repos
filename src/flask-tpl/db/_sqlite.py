import sqlite3
import threading


class SQLiteProxy:
    def __init__(self, path: str) -> None:
        self.path = path
        self.mutex = threading.Lock()
        self.conn = None

    def connect(self):
        with self.mutex:
            if self.conn is None:
                self.conn = sqlite3.connect(
                    database=self.path,
                    check_same_thread=True,
                    detect_types=sqlite3.PARSE_DECLTYPES,
                    autocommit=False,
                )
                self.conn.row_factory = sqlite3.Row
            return self.conn

    def close(self):
        with self.mutex:
            if self.conn is not None:
                self.conn.close()
                self.conn = None

    def execute(self, sql: str, params: tuple = None):
        self.connect()
        with self.mutex:
            cursor = self.conn.cursor()
            cursor = cursor.execute(sql, params or ())
            self.conn.commit()
            return cursor

    def executescript(self, sqltext: str):
        self.connect()
        with self.mutex:
            cursor = self.conn.cursor()
            cursor.executescript(sqltext)
            self.conn.commit()
            return cursor


if __name__ == "__main__":
    proxy = SQLiteProxy("test.sqlite3")
    proxy.execute("CREATE TABLE IF NOT EXISTS t_user (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
