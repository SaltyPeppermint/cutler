from dataclasses import dataclass, replace

import ffmpeg

@dataclass
class ForceFmt:
    fmt: str

    def filterify(self, blerg):
        strm = ffmpeg.filter(blerg.strm, 'format', self.fmt)
        return replace(blerg, strm=strm)
