from dataclasses import dataclass

import ffmpeg

@dataclass
class ForceFmt:
    fmt: str

    def filterify(self, strm):
        return ffmpeg.filter(strm, 'format', self.fmt)
