from redislite import Redis
from contextlib import contextmanager

from .abstract import ResourcePool
from .options import RedisOptions


class RedisConnectionPool(ResourcePool):
    __slots__ = ()

    def __init__(
        self,
        options: RedisOptions | None = None,
        **kwargs
    ):
        if not options:
            options = RedisOptions(**kwargs)

        self._options = options
        self._pool = Redis(**self._options)


    @contextmanager
    def acquire(self):
        yield self._pool

    def release(self):
        pass

    def get_connection(self):
        return self._pool

    def create_connection(self):
        pass

    def close(self):
        self._pool.connection_pool.disconnect()
        self._pool.connection_pool.close()

    def _initialize_pool(self):
        pass