__all__ = "SQLiteConnectionPool",

import atexit
import time
from datetime import timedelta
from queue import Queue
from threading import Lock, current_thread
from contextlib import contextmanager
from collections import defaultdict

from .abstract import ResourcePool
from .resources import SQLiteConnection

MAIN_THREAD_ID = current_thread().ident

class SQLiteConnectionPool(ResourcePool):
    __slots__ = ("_db_name", "_pools", "_locks")

    def __init__(self, db_name, max_connections=None):
        self._db_name = db_name
        self._max_connections = defaultdict(lambda: max_connections or 5)
        self._pools = defaultdict(lambda: Queue(max_connections))
        self._locks = defaultdict(Lock)
        self._n_connections = defaultdict(int)
        atexit.register(self.close)

    def __enter__(self):
        print(f"Entering pool: {self.thread_id}")
        return self.pool

    def __exit__(self, exc_type, exc_value, traceback):
        okay = True
        if exc_type is not None:
            okay = False
        print(f"Closing pool: {self.thread_id}")
        self.close_pool(thread_id=self.thread_id)
        print(f"Pool closed: {self.thread_id}")
        return okay

    @property
    def db_name(self):
        return self._db_name

    @property
    def lock(self):
        return self._locks[self.thread_id]

    @property
    def pool(self):
        return self._pools[self.thread_id]

    @property
    def max_connections(self):
        return self._max_connections[self.thread_id]

    @property
    def n_connections(self):
        return self._n_connections[self.thread_id]

    def set_max_connections(self, max_connections, thread_id=None):
        if thread_id:
            self._max_connections[thread_id] = max_connections
            pool = self.pool
            new_pool = Queue(max_connections)
            lock = self.lock
            with lock:
                while not pool.empty():
                    new_pool.put(pool.get())
                self._pools[thread_id] = new_pool
        else:
            for thread_id in self._pools.keys():
                self.set_max_connections(max_connections, thread_id)

    def get_connection(self, timeout=30):
        if isinstance(timeout, (float, int, timedelta)):
            if isinstance(timeout, timedelta):
                timeout = timeout.total_seconds()
            start = time.time()

        pool = self.pool
        lock = self.lock

        with lock:
            # If pool is empty
            if pool.empty():
                if self.n_connections < self.max_connections:
                    conn = self.create_connection()
                else:
                    lock.release()
                    print(f"Releasing lock from {self.thread_id}: {pool.qsize()}/{self.max_connections}")
                    while pool.empty():
                        time.sleep(0.1)
                        #print(f"Waiting for a connection: {self.thread_id}: {pool.qsize()}/{self.max_connections}")
                        if timeout and time.time() - start >= timeout:
                            raise TimeoutError("Timed out waiting for a connection")
                    lock.acquire()
            else:
                conn = pool.get()
        return conn

    def get_pool(self, thread_id):
        return self._pools[thread_id]

    def _get_pool_and_lock(self, thread_id):
        return self._pools[thread_id], self._locks[thread_id]

    @contextmanager
    def acquire(self):
        conn = self.get_connection()
        try:
            yield conn
        finally:
            self.release(conn)

    def create_connection(self, thread_id=None):
        thread_id = thread_id or self.thread_id
        self._n_connections[thread_id] += 1
        return SQLiteConnection(self._db_name)

    def release(self, conn):
        pool = self.pool
        lock = self.lock

        with lock:
            print(f"Releasing connection: {self.thread_id}: {pool.qsize()}/{self.max_connections}")
            pool.put(conn)
            print(f"Connection released: {self.thread_id}: {pool.qsize()}/{self.max_connections}")

    def close(self):
        thread_ids = tuple(self._pools.keys())
        for thread_id in thread_ids:
            self.close_pool(thread_id)

    def close_pool(self, thread_id):
        pool = self.pool
        lock = self.lock

        with lock:
            while not pool.empty():
                conn = pool.get()
                conn.close()
                self._n_connections[thread_id] -= 1
            del self._pools[thread_id]
            del self._locks[thread_id]

    def _initialize_pool(self):
        pass
