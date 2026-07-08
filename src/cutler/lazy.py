from typing import Callable

class Lazy[T]:
    def __init__(self, f):
        self._f = f
        self._computed = False
        self._val = None

    def get(self) -> T:
        if self._computed:
            return self._val

        self._val = self._f()
        return self._val

    def map[Q](self, g: Callable[[T], Q]) -> "Lazy[Q]":
        return Lazy(lambda: g(self.get()))
