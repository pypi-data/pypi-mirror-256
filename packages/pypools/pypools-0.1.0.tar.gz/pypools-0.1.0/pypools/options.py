__all__ = "RedisOptions",

from dataclasses import dataclass
from typing import Callable
from pathlib import Path

from redis import ConnectionPool as _RedisConnectionPool
from redis.retry import Retry as RedisRetry

@dataclass(slots=True)
class BaseOptions:
    _attrs: set                                         = None

    def __post_init__(self):
        self._attrs = set(key for key in self.__slots__ if not key.startswith("_"))

    def __iter__(self):
        for key in self._attrs:
            yield key, getattr(self, key)

    def __getitem__(self, key: str):
        return getattr(self, key)

    def keys(self):
        return self._attrs

    def discard(self, key):
        self._attrs.discard(key)

    def update(self, key, value):
        setattr(self, key, value)
        self._attrs.add(key)


@dataclass(slots=True)
class RedisOptions(BaseOptions):
    host: str | None                                    = None
    port: int | str | None                              = None
    unix_socket_path: Path | str | None                 = None
    db: int                                             = 0
    password: str | None                                = None
    socket_timeout: int | float | None                  = None
    socket_connect_timeout: int | float | None          = None
    socket_keepalive: int | float | None                = None
    socket_keepalive_options: dict | None               = None
    connection_pool: _RedisConnectionPool | None        = None
    encoding: str                                       = 'utf-8'
    encoding_errors: str                                = 'strict'
    charset: str | None                                 = None
    errors: str | None                                  = None
    decode_responses: bool                              = False
    retry_on_timeout: bool                              = False
    retry_on_error: list[Exception] | None              = None
    ssl: bool                                           = False
    ssl_keyfile: Path | str | None                      = None
    ssl_certfile: Path | str | None                     = None
    ssl_cert_reqs: str                                  = 'required'
    ssl_ca_certs: Path | str | None                     = None
    ssl_ca_path: Path | str | None                      = None
    ssl_ca_data: Path | str | None                      = None
    ssl_check_hostname: bool                            = False
    ssl_password: str | None                            = None
    ssl_validate_ocsp: bool                             = False
    ssl_validate_ocsp_stapled: bool                     = False
    ssl_ocsp_context: object | None                     = None
    ssl_ocsp_expected_cert: object | None               = None
    max_connections: int | None                         = None
    single_connection_client: bool                      = False
    health_check_interval: int | float                  = 0
    client_name: str | None                             = None
    lib_name: str                                       = 'redis-py'
    lib_version: str                                    = '99.99.99'
    username: str | None                                = None
    retry: RedisRetry | None                            = None
    redis_connect_func: Callable | None                 = None
    credential_provider: Callable | object | None       = None
    protocol: int                                       = 3
    serverconfig: dict | None                           = None
    dbfilename: Path | str | None                       = None

    def __post_init__(self):
        BaseOptions.__post_init__(self)

        if self.serverconfig is None:
            # Discard unused redislite options
            self.discard("serverconfig")

        if self.dbfilename is None:
            # Discard unused redislite options
            self.discard("dbfilename")

        if all((
            self.host is None,
            self.port is None,
            self.unix_socket_path is None,
        )):
            # Creating a new redislite server
            self.discard("host")
            self.discard("port")
            return

        if self.host or self.port:
            # Connecting to an existing redis server
            self.discard("unix_socket_path")
            self.discard("serverconfig")
            self.discard("dbfilename")
            return

        if self.unix_socket_path:
            path = Path(self.unix_socket_path)
            if path.exists():
                # Connecting to an existing redis server
                self.discard("dbfilename")
                self.discard("serverconfig")
                self.update("host", None)
                self.update("port", None)
            else:
                # Creating a new redislite server
                self.discard("host")
                self.discard("port")
