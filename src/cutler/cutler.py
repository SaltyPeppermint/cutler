import ffmpeg
import sys
from functools import reduce

from cutler.data import Chain, Source, Job
from cutler.lazy import Lazy
from cutler.filters import ResetTimebase

def render_job(job: Job):
    chain_results = {
        chain_name: Lazy(lambda: exec_chain(chain_name, chain, chain_results))
        for chain_name, chain in job.chains.items()
    }

    out_src = chain_results[job.out].get()

    out = ffmpeg.output(flt.strm, job.out_filename)
    out = ffmpeg.overwrite_output(out)
    return out.get_args()

def exec_chain(name: str, chain: Chain, chain_results: dict[str, Lazy[Source]]):
    print(f'chain {name} wants inputs {','.join(chain.inputs)}')
    input_srcs = [chain_results[inp].get() for inp in chain.inputs]

    src = chain.filters[0].filterify(*input_srcs)
    for fltr in chain.filters[1:]:
        src = fltr.filterify(src)

    return src
