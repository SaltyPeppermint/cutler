import ffmpeg
import shlex
import sys
import os
from functools import reduce

from cutler.data import Chain, Source, Job, Recipe
from cutler.lazy import Lazy
from cutler.filters import ResetTimebase
from cutler.cmd_exec import exec_cmd

def exec_recipe(recipe: Recipe):
    for job in recipe.jobs:
        render_job(job)

def render_job(job: Job):
    chain_results = {
        chain_name: Lazy(
            lambda chain=chain:
                exec_chain(chain, chain_results)
        )
        for chain_name, chain in job.chains.items()
    }

    out_strms = [chain_results[out].get().strm for out in job.outs]

    out = ffmpeg.output(*out_strms, job.out_filename, **job.out_opts)
    out = ffmpeg.overwrite_output(out)
    args = ['ffmpeg'] + out.get_args()

    exec_cmd(f'ffmpeg render {os.path.basename(job.out_filename)}', args)

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
