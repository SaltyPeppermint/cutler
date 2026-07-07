import click
import shlex

from cutler import cutler as cl


@click.command()
def main():
    intro = cl.Source(
        filename='balkan-ruby-intro.mov',
        filters=[
            cl.ForceFmtFilter(fmt='yuv420p'),
            cl.ScaleFilter(w=1920, h=1080),
        ],
    )
    talk = cl.Source(
        filename='raws/day1_f01.mp4',
        filters=[
            cl.TrimFilter(
                start=23 * 60 + 23,
                end=29 * 60 + 53,
            ),
        ],
    )
    sources = [talk, intro]
    job = cl.Job(sources=sources, out_filename='dedo.mp4')
    args = cl.render_job(job)

    print(shlex.join(['ffmpeg'] + args))

if __name__ == "__main__":
    main()
