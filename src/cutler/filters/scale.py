from dataclasses import dataclass, replace
from typing import Optional

import ffmpeg

@dataclass
class Scale:
    w: Optional[int] = None
    h: Optional[int] = None

    def filterify(self, source):
        w = self.w
        h = self.h
        if w is None and h is None:
            raise RuntimeError('please specify w and/or h')

        if w is None:
            w = -1
        if h is None:
            h = -1

        strm = ffmpeg.filter(source.strm, 'scale', w, h)
        return replace(source, strm=strm)
