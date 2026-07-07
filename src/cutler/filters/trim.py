from dataclasses import dataclass
from typing import Optional, Union

import ffmpeg

@dataclass
class Trim:
    start: Optional[float] = None               # seconds, None = beginning of file
    end: Optional[float] = None                 # seconds, None = end of file
    duration: Optional[float] = None            # alternative to end; ignored if end is set
    kind: Union['ts', 'pts', 'frame'] = 'ts'    # whether to interpret offsets as timestamp, timecode or frame number

    def filterify(self, strm):
        args = {
            'start': self.start,
            'end': self.end,
        }
        if self.end is None and self.duration is not None:
            args['end'] = self.end + self.duration

        if self.kind == 'ts':
            suffix = ''
        elif self.kind == 'pts':
            suffix = '_pts'
        elif self.kind == 'frame':
            suffix = '_frame'
        else:
            raise RuntimeError(f'unknown kind {self.kind}')

        args = {k + suffix: v for k, v in args.items() if v is not None}

        strm = ffmpeg.trim(strm, **args)
        return ffmpeg.filter(strm, 'setpts', 'PTS-STARTPTS')
