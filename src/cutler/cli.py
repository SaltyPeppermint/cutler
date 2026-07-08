import click
import shlex

from cutler import cutler as cl
from cutler import filters
from cutler import data


@click.command()
def main():
    chains = {
        'intro': cl.Chain(
            filters=[
                filters.ReadClip(filename='balkan-ruby-intro.mov'),
                filters.ForceFmt(fmt='yuv420p'),
                filters.ChangeFPS(fps=30),
                filters.Scale(w=1920, h=1080),
            ],
        ),
        'talk': cl.Chain(
            filters=[
                filters.ReadClip(filename='raws/day1_f01.mp4'),
                filters.Trim(
                    start=23 * 60 + 23,
                    end=29 * 60 + 53,
                ),
            ],
        ),
        'result': cl.Chain(
            inputs=['intro', 'talk'],
            filters=[
                filters.ConcatXFade(transitions=[
                    filters.Transition(
                        effect='vertclose',
                        duration=0.5,
                    )
                ]),
            ],
        )
    }
    job = cl.Job(chains=chains, out='result', out_filename='out/dedo.mp4')
    args = cl.render_job(job)

    print(shlex.join(['ffmpeg'] + args))

if __name__ == "__main__":
    main()
