import ffmpeg
import sys

from cutler.data import Source, Blerg, Job

def render_job(job):
    blergs = map(make_src_blerg, job.sources)
    blergs = map(filterify_blerg, blergs)
    flt = concat_blergs(blergs)
    out = ffmpeg.output(flt, job.out_filename)
    out = ffmpeg.overwrite_output(out)
    return out.get_args()

def concat_blergs(blergs):
    streams = [blerg.strm for blerg in blergs]
    streams = reversed(list(streams))     # wtf?
    return ffmpeg.concat(*streams)

def filterify_blerg(blerg):
    for fltr in blerg.src.filters:
        blerg = fltr.filterify(blerg)
    return blerg

def make_src_blerg(source):
    strm = ffmpeg.input(source.filename)    # TODO: take loop into account

    try:
        probe = ffmpeg.probe(source.filename)
    except ffmpeg.Error as e:
        sys.stderr.write(e.stderr.decode('utf-8'))
        raise

    return Blerg(
        src=source,
        strm=strm,
        probe=probe,
        actual_duration=probe['format']['duration'],
    )
