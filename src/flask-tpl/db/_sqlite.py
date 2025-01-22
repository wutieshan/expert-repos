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
                    check_same_thread=False,
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
    
    def start_transaction(self):
        self.conn.execute("begin transaction")
    
    def commit(self):
        self.conn.commit()
    
    def roolback(self):
        self.conn.rollback()

    def execute(self, sql: str, params: tuple = None, autocommit: bool = True):
        self.connect()
        with self.mutex:
            if autocommit:
                self.start_transaction()
                cursor = self.conn.execute(sql, params or ())
                self.commit()
            else:
                cursor = self.conn.execute(sql, params or ())
            return cursor

    def executescript(self, sqltext: str):
        self.connect()
        with self.mutex:
            self.start_transaction()
            cursor = self.conn.executescript(sqltext)
            self.commit()
            return cursor


if __name__ == "__main__":
    proxy = SQLiteProxy(":memory:")
    with open("./src/flask-tpl/db/schema-ddl.sql", "r", encoding="utf8") as fp:
        proxy.executescript(fp.read())
