from dataclasses import dataclass, replace

import ffmpeg

@dataclass
class ForceFmt:
    fmt: str

    def filterify(self, source):
        strm = ffmpeg.filter(source.strm, 'format', self.fmt)
        return replace(source, strm=strm)
