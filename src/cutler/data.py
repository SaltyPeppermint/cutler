import ffmpeg
from dataclasses import dataclass, field

@dataclass
class Transition:
    effect: str = 'fade'
    duration: float = 0

@dataclass
class Source:
    # TODO: instead of loop, start, end, etc, add a list of filters to apply to this source
    filename: str
    loop: bool      = False                         # use if source is image
    filters: list() = field(default_factory = list) # TODO: separate audio filter chain?
    transition: Transition = field(default_factory = Transition)

@dataclass
class Blerg:   # TODO: naming hard
    strm: ffmpeg.Stream
    transition: Transition
    actual_duration: float

@dataclass
class Job:
    sources: list[Source]
    out_filename: str
    # TODO: add ffmpeg flags
