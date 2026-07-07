from dataclasses import dataclass, replace

import ffmpeg

@dataclass
class ResetTimebase:
    def filterify(self, blerg):
        strm = blerg.strm

        strm = ffmpeg.filter(strm, 'settb', 'AVTB')
        strm = ffmpeg.filter(strm, 'setpts', 'PTS-STARTPTS')

        return replace(blerg, strm=strm)
