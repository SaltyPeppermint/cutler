from dataclasses import dataclass
from typing import Optional

import ffmpeg

@dataclass
class Scale:
    w: Optional[int] = None
    h: Optional[int] = None

    def filterify(self, strm):
        w = self.w
        h = self.h
        if w is None and h is None:
            raise RuntimeError('please specify w and/or h')

        if w is None:
            w = -1
        if h is None:
            h = -1

        return ffmpeg.filter(strm, 'scale', w, h)
