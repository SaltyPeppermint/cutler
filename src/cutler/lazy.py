import inspect
from typing import Callable

class Lazy[T]:
    def __init__(self, f):
        self._f = f
        self._computed = False
        self._val = None

    async def get(self) -> T:
        if self._computed:
            return self._val

        val = self._f()
        if inspect.isawaitable(val):
            val = await val

        self._val = val
        self._computed = True
        return self._val
