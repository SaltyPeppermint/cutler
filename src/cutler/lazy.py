import asyncio
import inspect


class Lazy[T]:
    def __init__(self, f):
        self._f = f
        self._future: asyncio.Future[T] | None = None

    def get(self) -> asyncio.Future[T]:
        if self._future is None:
            self._future = asyncio.ensure_future(self._run())
        return self._future

    async def _run(self) -> T:
        val = self._f()
        if inspect.isawaitable(val):
            val = await val
        return val
