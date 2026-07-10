from dataclasses import dataclass, field
from typing import Any, Literal, Optional

import ffmpeg

from cutler.data import Source
from cutler.lazy import Lazy


@dataclass
class Lavfi:
    name: str
    params: dict[str, Any] = field(default_factory=dict)
    duration: Optional[float] = None
    kind: Literal["audio", "video", "av"] = "av"

    @staticmethod
    def ref():
        return "lavfi"

    async def filterify(self, ctx):
        kwargs = {}
        if self.duration is not None:
            kwargs["t"] = self.duration

        inp = self.name + "=" + ":".join([f"{k}={v}" for k, v in self.params.items()])

        strm = ffmpeg.input(inp, f="lavfi", **kwargs)

        return Source(
            strm=strm,
            actual_duration=Lazy(lambda: self.duration),
            kind=self.kind,
        )
