from dataclasses import dataclass
from typing import Optional
import json
import subprocess
import sys
import os

import ffmpeg

from cutler.data import Source
from cutler.lazy import Lazy

@dataclass
class ReadClip:
    filename: str = None
    gen_cmd: list[str] = None
    gen_overwrite: bool = True
    looped: bool = False
    fmt: Optional[str] = None
    seek_start: Optional[float] = None
    seek_end: Optional[float] = None
    duration: Optional[float] = None

    @staticmethod
    def ref():
        return 'read_clip'

    def filterify(self):
        if self.gen_cmd is not None:
            if self.filename is None or not os.path.exists(self.filename) or self.gen_overwrite:
                result = subprocess.run(self.gen_cmd, capture_output=True, text=True, check=True)

                if self.filename is None:
                    self.filename = result.stdout.strip()
        elif self.filename is None:
            raise RuntimeError('either filename or gen_cmd must be provided')

        duration = self.duration

        if self.seek_end is not None:
            if duration is not None:
                raise RuntimeError('cannot specify both seek_start and duration')
            duration = self.seek_end - (self.seek_start or 0)

        kwargs = {}
        if self.fmt is not None:
            kwargs['f'] = self.fmt
        if duration is not None:
            kwargs['t'] = duration
        if self.seek_start is not None:
            kwargs['ss'] = self.seek_start

        strm = ffmpeg.input(self.filename, **kwargs)
        if self.looped:
            raise RuntimeError('not implemented (FIXME: pass loop arg to ffmpeg for this input)')

        probe = Lazy(lambda: self._ffprobe())
        if duration is None:
            duration_lazy = Lazy(lambda: float(probe.get()['format']['duration']))
        else:
            duration_lazy = Lazy(lambda: duration)

        return Source(
            strm=strm,
            actual_duration=duration_lazy,
            ffprobe_result = probe,
            kind='av',
        )

    def _ffprobe(self):
        args = ['ffprobe', '-show_format', '-show_streams', '-of', 'json', self.filename]
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            sys.stderr.write(e.stderr)
            raise
        return json.loads(result.stdout)
