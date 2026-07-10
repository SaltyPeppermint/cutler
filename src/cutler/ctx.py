import asyncio

from cutler.data import Settings


class Ctx:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cmd_semaphore = asyncio.Semaphore(self.settings.max_parallel_cmds)
