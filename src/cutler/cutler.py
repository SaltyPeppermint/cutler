import ffmpeg
import shlex
import sys
from functools import reduce

from cutler.data import Chain, Source, Job, Recipe
from cutler.lazy import Lazy
from cutler.filters import ResetTimebase

def exec_recipe(recipe: Recipe):
    for job in recipe.jobs:
        args = render_job(job)
        print(shlex.join(['ffmpeg'] + args))    # will actually execute later

def render_job(job: Job):
    chain_results = {
        chain_name: Lazy(
            lambda chain=chain:
                exec_chain(chain, chain_results)
        )
        for chain_name, chain in job.chains.items()
    }

    out_strms = [chain_results[out].get().strm for out in job.outs]

    out = ffmpeg.output(*out_strms, job.out_filename)
    out = ffmpeg.overwrite_output(out)
    return out.get_args()

def get_chain_result(chain_results: dict[str, Lazy[Source]], ref):
    if '.' in ref:
        name, branch = ref.split('.', 2)
    else:
        name, branch = ref, ''

    return chain_results[name].get().branch(branch)

def exec_chain(chain: Chain, chain_results: dict[str, Lazy[Source]]):
    input_srcs = [get_chain_result(chain_results, inp) for inp in chain.inputs]

    src = chain.filters[0].filterify(*input_srcs)
    for fltr in chain.filters[1:]:
        src = fltr.filterify(src)

    return src
