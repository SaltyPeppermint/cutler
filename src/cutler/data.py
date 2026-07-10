import ffmpeg
from dataclasses import dataclass, field, replace
from typing import Protocol, Union, runtime_checkable, Optional
from cutler.lazy import Lazy

@dataclass
class Source:   # TODO: naming hard
    strm: ffmpeg.Stream
    actual_duration: Optional[Lazy[float]]
    kind: Union['audio', 'video', 'av']
    branches: dict[str, ffmpeg.Stream] = field(default_factory = dict)
    ffprobe_result: Optional[Lazy[dict()]] = None

    def branch(self, name=None):
        if not name:
            return self
        else:
            return replace(self, strm=self.branches[name], branches={})

@runtime_checkable
class Filter(Protocol):
    def filterify(self, ctx, *srcs: Source) -> Source: ...

@dataclass
class Chain:
    inputs: list[str] = field(default_factory = list)   # chain inputs are names of other chains
    filters: list[Filter] = field(default_factory = list)

@dataclass
class Job:
    chains: dict[str, Chain]
    outs: list[str]    # names of chains whose outputs will be included in output video
    out_filename: str
    out_opts: dict[str, any]

@dataclass
class Settings:
    max_parallel_cmds: int = 8  # determined by fair dice roll
    # command overrides may be either a string (simple command) or list (command with args)
    command_override: dict[str, any] = field(default_factory=dict)

@dataclass
class Recipe:
    jobs: list[Job]
    settings: Settings
