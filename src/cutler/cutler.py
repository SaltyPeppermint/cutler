import ffmpeg
import sys
from functools import reduce

from cutler.data import Clip, Source, Job
from cutler.filters import ResetTimebase

def render_job(job):
    sources = map(clip_to_src, job.clips)
    flt = reduce(concat_sources, sources)
    out = ffmpeg.output(flt.strm, job.out_filename)
    out = ffmpeg.overwrite_output(out)
    return out.get_args()

def concat_sources(l, r):
    strm = ffmpeg.filter(
        [l.strm, r.strm],
        'xfade',
        transition=l.transition.effect,
        duration=l.transition.duration,
        offset=l.actual_duration - l.transition.duration,
    )
    return Source(
        strm=strm,
        transition=r.transition,
        actual_duration=l.actual_duration + r.actual_duration - l.transition.duration,
    )


def clip_to_src(clip):
    strm = ffmpeg.input(clip.filename)    # TODO: take loop into account

    try:
        probe = ffmpeg.probe(clip.filename)
    except ffmpeg.Error as e:
        sys.stderr.write(e.stderr.decode('utf-8'))
        raise

    source = Source(
        strm=strm,
        transition=clip.transition,
        actual_duration=float(probe['format']['duration']),
    )

    for fltr in clip.filters + [ResetTimebase()]:
        source = fltr.filterify(source)


    return source

