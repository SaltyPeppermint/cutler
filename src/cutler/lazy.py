import asyncio
import inspect

class Lazy[T]:
    def __init__(self, f):
        self._f = f
        self._computed = False
        self._val = None
        self._lock = asyncio.Lock()

    async def get(self) -> T:
        if self._computed:
            return self._val

        async with self._lock:
            # another get() may have computed the value while we waited for the lock
            if self._computed:
                return self._val

            val = self._f()
            if inspect.isawaitable(val):
                val = await val

            self._val = val
            self._computed = True
            return self._val
