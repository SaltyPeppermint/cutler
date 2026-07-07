import click
import shlex

from cutler import cutler as cl
from cutler import filters
from cutler import data


@click.command()
def main():
    intro = cl.Clip(
        filename='balkan-ruby-intro.mov',
        filters=[
            filters.ForceFmt(fmt='yuv420p'),
            filters.ChangeFPS(fps=30),
            filters.Scale(w=1920, h=1080),
        ],
        transition=data.Transition(
            duration=0.5
        ),
    )
    talk = cl.Clip(
        filename='raws/day1_f01.mp4',
        filters=[
            filters.Trim(
                start=23 * 60 + 23,
                end=29 * 60 + 53,
            ),
        ],
    )
    clips = [intro, talk]
    job = cl.Job(clips=clips, out_filename='out/dedo.mp4')
    args = cl.render_job(job)

    print(shlex.join(['ffmpeg'] + args))

if __name__ == "__main__":
    main()
