from dataclasses import dataclass, replace, field
from typing import Any

import ffmpeg


@dataclass
class RawFFmpegFilter:
    name: str
    args: list[Any] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def ref():
        return "raw_ffmpeg_filter"

    async def filterify(self, ctx, *srcs):
        strms = [src.strm for src in srcs]
        strm = ffmpeg.filter(strms, self.name, *self.args, **self.kwargs)
        return replace(srcs[0], strm=strm)
