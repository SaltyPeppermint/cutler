from dataclasses import dataclass, replace

import ffmpeg

@dataclass
class ChangeFPS:
    fps: float

    @staticmethod
    def ref():
        return 'change_fps'

    def filterify(self, source):
        strm = ffmpeg.filter(source.strm, 'fps', self.fps)
        return replace(source, strm=strm)
