from rich.console import Group
from rich.live import Live
from rich.text import Text


class Display:
    """
    This file was produced by an LLM and cannot be trusted.

    Here is some slop text:

    A live, scroll-friendly view of running commands.

    Each in-flight command is shown as `name: <last output line>` in a live
    region pinned to the bottom of the terminal, updated in realtime. When a
    command finishes, its line is emitted as permanent output (`name - done`)
    *above* the live region and removed from it -- so completed work scrolls into
    history normally and, once everything is done, the live region is empty and
    the terminal stays fully scrollable (we never use the alternate screen).
    """

    def __init__(self):
        self._active = {}  # key -> [name, last_line]
        self._order = []
        self._counter = 0
        self._live = Live(
            self._render(),
            transient=True,  # the (empty) live region is cleared on stop
            refresh_per_second=12,
        )
        self._started = False

    def _render(self):
        lines = []
        for key in self._order:
            name, last = self._active[key]
            line = Text.assemble((f"{name}: ", "bold cyan"), last)
            line.no_wrap = True
            line.overflow = "ellipsis"
            lines.append(line)
        return Group(*lines)

    def __enter__(self):
        self._live.start()
        self._started = True
        return self

    def __exit__(self, *exc):
        self.stop()

    def stop(self):
        if self._started:
            self._live.stop()
            self._started = False

    def add(self, name):
        key = self._counter
        self._counter += 1
        self._active[key] = [name, ""]
        self._order.append(key)
        self._live.update(self._render())
        return key

    def update(self, key, last_line):
        self._active[key][1] = last_line
        self._live.update(self._render())

    def done(self, key):
        name = self._active.pop(key)[0]
        self._order.remove(key)
        # permanent line, printed above the live region so it scrolls into history
        self._live.console.print(Text.assemble((name, "bold green"), (" - done", "green")))
        self._live.update(self._render())
