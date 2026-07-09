from dataclasses import dataclass, replace, field

import ffmpeg

@dataclass
class RawFFmpegFilter:
    name: str
    args: list[any] = field(default_factory = list)
    kwargs: dict[str, any] = field(default_factory = dict)

    @staticmethod
    def ref():
        return 'raw_ffmpeg_filter'

    async def filterify(self, *srcs):
        strms = [src.strm for src in srcs]
        strm = ffmpeg.filter(strms, self.name, *self.args, **self.kwargs)
        return replace(srcs[0], strm=strm)
