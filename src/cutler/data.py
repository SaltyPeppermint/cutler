import ffmpeg
from dataclasses import dataclass, field

@dataclass
class Chain:
    inputs: list[str] = field(default_factory = list)   # chain inputs are names of other chains
    filters: list() = field(default_factory = list)

@dataclass
class Source:   # TODO: naming hard
    strm: ffmpeg.Stream
    actual_duration: float

@dataclass
class Job:
    chains: dict[str, Chain]
    out: str    # name of the chain that produces the job output
    out_filename: str
    # TODO: add ffmpeg flags
