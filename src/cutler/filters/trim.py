from dataclasses import dataclass, replace
from typing import Optional, Union

import ffmpeg

@dataclass
class Trim:
    start: Optional[float] = None               # seconds, None = beginning of file
    end: Optional[float] = None                 # seconds, None = end of file
    duration: Optional[float] = None            # alternative to end; ignored if end is set
    kind: Union['ts', 'pts', 'frame'] = 'ts'    # whether to interpret offsets as timestamp, timecode or frame number

    def filterify(self, blerg):
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

        if self.kind == 'frame':
            raise RuntimeError("don't know how to compute duration of frame-based trim, FIXME")

        if self.duration is not None:
            actual_duration = self.duration
        elif self.end is None and self.start is None:
            actual_duration = blerg.actual_duration
        elif self.end is None:
            if self.kind == 'pts':
                raise RuntimeError("don't know how to compute duration of PTS-based trim with no end, FIXME")
            actual_duration = blerg.actual_duration - self.start
        elif self.start is None:
            if self.kind == 'pts':
                raise RuntimeError("don't know how to compute duration of PTS-based trim with no start, FIXME")
            actual_duration = self.end
        else:
            actual_duration = self.end - self.start

        return replace(blerg,
            strm=ffmpeg.trim(blerg.strm, **args),
            actual_duration=actual_duration,
        )
