from dataclasses import dataclass, field

import ffmpeg

@dataclass
class Source:
    # TODO: instead of loop, start, end, etc, add a list of filters to apply to this source
    filename: str
    loop: bool      = False                         # use if source is image
    filters: list() = field(default_factory = list) # TODO: separate audio filter chain?

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
    streams = map(filterify_source, sources)
    streams = reversed(list(streams))     # wtf?
    return ffmpeg.concat(*streams)

def filterify_source(source):
    strm = ffmpeg.input(source.filename)    # TODO: take loop into account
    for fltr in source.filters:
        strm = fltr.filterify(strm)
    return strm
