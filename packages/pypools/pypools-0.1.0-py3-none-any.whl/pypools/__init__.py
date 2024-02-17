__all__ = "ResourcePool", "Resource", "SQLiteConnectionPool", "RedisConnectionPool", "SQLiteConnection", "RedisConnection", "InMemoryConnection", "sqlite_connection_factory", "redis_connection_factory", "memory_connection_factory"

from threading import current_thread

from .abstract import ResourcePool
from .resources import *
from .sqlite import SQLiteConnectionPool
from .redis import RedisConnectionPool
from .memory import InMemoryConnectionPool
from .options import *

MAIN_THREAD_ID = current_thread().ident