import json

from cutler import cutler as cl
from cutler import filters

def parse_recipe(data: dict) -> cl.Recipe:
    jobs = [parse_job(jobdata) for jobdata in data['jobs']]
    return cl.Recipe(jobs=jobs)

def parse_job(job: dict) -> cl.Job:
    chains = {
        name: parse_chain(chain)
        for name, chain in job['chains'].items()
    }

    return cl.Job(
        chains=chains,
        outs=job['outs'],
        out_filename=job['out_filename'],
        out_opts=job.get('out_opts', {}),
    )

def parse_chain(chain: dict) -> cl.Chain:
    return cl.Chain(
        inputs=chain.get('inputs', []),
        filters=[parse_filter(f) for f in chain['filters']],
    )

def parse_filter(spec: dict):
    kwargs = dict(spec)
    ref = kwargs.pop('ref')
    args = kwargs.pop('args', [])

    cls = filters.by_ref.get(ref)
    if cls is None:
        return filters.RawFFmpegFilter(name=ref, args=args, kwargs=kwargs)

    from_dict = getattr(cls, 'from_dict', None)
    if from_dict is not None:
        return from_dict(kwargs)

    return cls(*args, **kwargs)
