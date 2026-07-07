from dataclasses import dataclass, replace

import ffmpeg

@dataclass
class ChangeFPS:
    fps: float

    def filterify(self, blerg):
        strm = ffmpeg.filter(blerg.strm, 'fps', self.fps)
        return replace(blerg, strm=strm)
