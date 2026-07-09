import asyncio
import ffmpeg
import shlex
import sys
import os
from functools import reduce

from cutler.data import Chain, Source, Job, Recipe
from cutler.lazy import Lazy
from cutler.filters import ResetTimebase
from cutler.cmd_exec import exec_cmd

async def exec_recipe(recipe: Recipe):
    for job in recipe.jobs:
        await render_job(job)

async def render_job(job: Job):
    chain_results = {
        chain_name: Lazy(
            lambda chain=chain:
                exec_chain(chain, chain_results)
        )
        for chain_name, chain in job.chains.items()
    }

    out_results = await get_chain_results(chain_results, job.outs)
    out_strms = [r.strm for r in out_results]

    out = ffmpeg.output(*out_strms, job.out_filename, **job.out_opts)
    out = ffmpeg.overwrite_output(out)
    args = ['ffmpeg'] + out.get_args()

    await exec_cmd(f'ffmpeg render {os.path.basename(job.out_filename)}', args)

async def exec_chain(chain: Chain, chain_results: dict[str, Lazy[Source]]):
    input_srcs = await get_chain_results(chain_results, chain.inputs)

    src = await chain.filters[0].filterify(*input_srcs)
    for fltr in chain.filters[1:]:
        src = await fltr.filterify(src)

    return src

async def get_chain_results(chain_results: dict[str, Lazy[Source]], refs: list[str]):
    return await asyncio.gather(*(get_chain_result(chain_results, ref) for ref in refs))

async def get_chain_result(chain_results: dict[str, Lazy[Source]], ref):
    if '.' in ref:
        name, branch = ref.split('.', 2)
    else:
        name, branch = ref, ''

    return (await chain_results[name].get()).branch(branch)
