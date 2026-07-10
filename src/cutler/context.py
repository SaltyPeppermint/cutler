import asyncio

from cutler.data import Settings
from cutler.display import Display


class Ctx:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cmd_semaphore = asyncio.Semaphore(settings.max_parallel_cmds)
        self.display = Display()

    def __enter__(self):
        self.display.__enter__()
        return self

    def __exit__(self, *exc):
        self.display.__exit__(*exc)


def new(settings: Settings) -> Ctx:
    return Ctx(settings)
