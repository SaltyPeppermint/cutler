import ffmpeg
from dataclasses import dataclass, field

@dataclass
class Transition:
    effect: str = 'fade'
    duration: float = 0

@dataclass
class Clip:
    # TODO: instead of loop, start, end, etc, add a list of filters to apply to this clip
    filename: str
    loop: bool      = False                         # use if clip is image
    filters: list() = field(default_factory = list) # TODO: separate audio filter chain?
    transition: Transition = field(default_factory = Transition)

@dataclass
class Source:   # TODO: naming hard
    strm: ffmpeg.Stream
    transition: Transition
    actual_duration: float

@dataclass
class Job:
    clips: list[Clip]
    out_filename: str
    # TODO: add ffmpeg flags
