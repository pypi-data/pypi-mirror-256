__all__ = "SQLiteConnection",

from sqlite3 import connect as sqlite_connect
from threading import Lock, current_thread
from time import time

from .abstract import Resource

class SQLiteConnection(Resource):
    lock = Lock()

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite_connect(db_name)
        self.cursor = self.conn.cursor()
        self._thread_id = self.thread.ident
        self._last_use = time()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

    def __del__(self):
        self.conn.close()

    def close(self):
        self.conn.close()

    @property
    def thread(self):
        return current_thread()

    def commit(self):
        self.conn.commit()

    def create_table(self, name, columns, commit=False):
        with self:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({columns})")
        if commit:
            self.conn.commit()
        self._last_use = time()

    def delete(self, sql, params, commit=False):
        with self:
            self.cursor.execute(sql, params)
        if commit:
            self.conn.commit()
        self._last_use = time()

    def insert(self, sql, params, commit=False):
        with self:
            self.cursor.execute(sql, params)
        if commit:
            self.conn.commit()
        self._last_use = time()

    def select(self, sql, params, commit=False):
        with self:
            self.cursor.execute(sql, params)
            results =  self.cursor.fetchall()
        self._last_use = time()
        if commit:
            self.conn.commit()
        return results

    def _reconnect(self):
        self.conn.close()
        self.conn = sqlite_connect(self.db_name)
        self.cursor = self.conn.cursor()
