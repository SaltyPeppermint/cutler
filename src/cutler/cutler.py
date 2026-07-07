import subprocess
from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoSource:
    # TODO: instead of loop, start, end, etc, add a list of filters to apply to this source
    filename: str
    loop: bool  # use if source is image
    start: Optional[float] = None  # seconds, None = beginning of file
    end: Optional[float] = None    # seconds, None = end of file
    duration: Optional[float] = None  # alternative to end; ignored if end is set

# TODO: make a FilterComplex class that lets you use keys for streams

def concat_video_segments(
    sources: list[VideoSource],
    pre_flags: list[str] = (),
    post_flags: list[str] = (),
    output: str = "output.mp4",
):
    if not sources:
        raise ValueError("At least one source is required")

    SEEK_BUFFER = 10.0  # seconds before start to fast-seek to

    inputs = []
    for src in sources:
        start = src.start  # may be None

        if src.loop:
            inputs += ["-loop", "1"]
        if start is not None and start > SEEK_BUFFER:
            inputs += ["-ss", str(start - SEEK_BUFFER)]

        inputs += ["-i", src.filename]

    filter_parts = []
    segment_labels = []

    for i, src in enumerate(sources):
        start = src.start
        end = src.end

        if end is None and src.duration is not None and start is not None:
            end = start + src.duration
        elif end is None and src.duration is not None:
            end = src.duration

        trim_args = []
        atrim_args = []

        if start is not None:
            trim_args.append(f"start={start}")
            atrim_args.append(f"start={start}")
        if end is not None:
            trim_args.append(f"end={end}")
            atrim_args.append(f"end={end}")

        trim_expr  = "trim="  + ":".join(trim_args)  if trim_args else "trim"
        atrim_expr = "atrim=" + ":".join(atrim_args) if atrim_args else "atrim"

        vl = f"v{i}"
        al = f"a{i}"

        filter_parts.append(
            f"[{i}:v]{trim_expr},setpts=PTS-STARTPTS[{vl}]"
        )
        filter_parts.append(
            f"[{i}:a]{atrim_expr},asetpts=PTS-STARTPTS[{al}]"
        )
        segment_labels.append((vl, al))

    # concat filter
    n = len(sources)
    inputs = "".join(f"[{vl}][{al}]" for vl, al in segment_labels)
    filter_parts.append(f"{inputs}concat=n={n}:v=1:a=1[vout][aout]")

    filter_complex = ";\n  ".join(filter_parts)

    cmd = [
        "ffmpeg",
        *pre_flags,
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        *post_flags,
        output,
    ]

    # TODO: generate ninja script
    subprocess.run(cmd, check=True)
