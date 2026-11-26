import time


class TTLCache:
    def __init__(self, ttl=900):
        self.ttl = ttl
        self._items = {}

    def get(self, key):
        hit = self._items.get(key)
        if hit is None:
            return None
        expires, value = hit
        if expires < time.time():
            self._items.pop(key, None)
            return None
        return value

    def set(self, key, value):
        self._items[key] = (time.time() + self.ttl, value)
