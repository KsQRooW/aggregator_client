from typing import Any


class Cache:
    def __init__(self, max_items: int = 10):
        self._data = {}
        self._max_items = max_items

    @property
    def current_keys(self):
        return self._data.keys()

    def add_item(self, name: str, value: Any):
        self._data[name] = value
        if len(self._data) > self._max_items:
            self._data.pop(next(iter(self._data)))

    def get_item(self, name: str) -> Any:
        return self._data.get(name)
