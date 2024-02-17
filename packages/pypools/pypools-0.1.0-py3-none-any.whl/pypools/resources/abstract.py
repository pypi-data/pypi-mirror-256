from abc import ABC, abstractmethod
from threading import current_thread

class Resource(ABC):
    __slots__ = ("_thread_id", "_last_use")

    def __del__(self):
        self.close()

    @abstractmethod
    def close(self):
        pass

    @property
    def thread(self):
        return current_thread()

    @property
    def last_use(self):
        return self._last_use