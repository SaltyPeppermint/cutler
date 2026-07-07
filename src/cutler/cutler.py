from dataclasses import dataclass, field
from typing import Optional, Union

import ffmpeg

@dataclass
class Source:
    # TODO: instead of loop, start, end, etc, add a list of filters to apply to this source
    filename: str
    loop: bool      = False                         # use if source is image
    filters: list() = field(default_factory = list) # TODO: separate audio filter chain?

@dataclass
class TrimFilter:
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

@dataclass
class ForceFmtFilter:
    fmt: str

    def filterify(self, strm):
        return ffmpeg.filter(strm, 'format', self.fmt)

@dataclass
class ScaleFilter:
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

@dataclass
class Job:
    sources: list[Source]
    out_filename: str
    # TODO: add ffmpeg flags

# TODO: make a FilterComplex class that lets you use keys for streams

def render_job(job):
    flt = filterify_sources(job.sources)
    out = ffmpeg.output(flt, job.out_filename)
    out = ffmpeg.overwrite_output(out)
    return out.get_args()

def filterify_job(job):
    return filterify_sources(job.sources)

def filterify_sources(sources):
    return ffmpeg.concat(*map(filterify_source, sources))

def filterify_source(source):
    strm = ffmpeg.input(source.filename)    # TODO: take loop into account
    for fltr in source.filters:
        strm = fltr.filterify(strm)
    return strm
