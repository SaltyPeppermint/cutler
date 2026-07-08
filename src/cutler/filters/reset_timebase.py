from dataclasses import dataclass, replace

import ffmpeg

@dataclass
class ResetTimebase:
    @staticmethod
    def ref():
        return 'reset_timebase'

    def filterify(self, source):
        strm = source.strm

        strm = ffmpeg.filter(strm, 'settb', 'AVTB')
        strm = ffmpeg.filter(strm, 'setpts', 'PTS-STARTPTS')

        return replace(source, strm=strm)
