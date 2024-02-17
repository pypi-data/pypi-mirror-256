from .abstract import ResourcePool

class InMemoryConnectionPool(ResourcePool):
    def __init__(self):
        pass

    def acquire(self):
        pass

    def release(self, resource):
        pass

    def create_connection(self):
        pass

    def close(self):
        pass

    def _initialize_pool(self):
        pass