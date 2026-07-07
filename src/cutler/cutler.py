import ffmpeg
import sys
from functools import reduce

from cutler.data import Source, Blerg, Job
from cutler.filters import ResetTimebase

def render_job(job):
    blergs = map(make_src_blerg, job.sources)
    flt = reduce(concat_blergs, blergs)
    out = ffmpeg.output(flt.strm, job.out_filename)
    out = ffmpeg.overwrite_output(out)
    return out.get_args()

def concat_blergs(l, r):
    strm = ffmpeg.filter(
        [l.strm, r.strm],
        'xfade',
        transition=l.transition.effect,
        duration=l.transition.duration,
        offset=l.actual_duration - l.transition.duration,
    )
    return Blerg(
        strm=strm,
        transition=r.transition,
        actual_duration=l.actual_duration + r.actual_duration - l.transition.duration,
    )


def make_src_blerg(source):
    strm = ffmpeg.input(source.filename)    # TODO: take loop into account

    try:
        probe = ffmpeg.probe(source.filename)
    except ffmpeg.Error as e:
        sys.stderr.write(e.stderr.decode('utf-8'))
        raise

    blerg = Blerg(
        strm=strm,
        transition=source.transition,
        actual_duration=float(probe['format']['duration']),
    )

    for fltr in source.filters + [ResetTimebase()]:
        blerg = fltr.filterify(blerg)


    return blerg

