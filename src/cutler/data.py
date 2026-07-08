import ffmpeg
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

@dataclass
class Source:   # TODO: naming hard
    strm: ffmpeg.Stream
    actual_duration: float

@runtime_checkable
class Filter(Protocol):
    def filterify(self, *srcs: Source) -> Source: ...

@dataclass
class Chain:
    inputs: list[str] = field(default_factory = list)   # chain inputs are names of other chains
    filters: list[Filter] = field(default_factory = list)

@dataclass
class Job:
    chains: dict[str, Chain]
    out: str    # name of the chain that produces the job output
    out_filename: str
    # TODO: add ffmpeg flags

@dataclass
class Recipe:
    jobs: list[Job]
