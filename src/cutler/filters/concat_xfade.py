from dataclasses import dataclass

import ffmpeg

from cutler.data import Source
from cutler.filters.reset_timebase import ResetTimebase
from cutler.lazy import Lazy


@dataclass
class Transition:
    effect: str = "fade"
    duration: float = 0


@dataclass
class ConcatXFade:
    transitions: list[Transition]

    @staticmethod
    def ref():
        return "concat_xfade"

    @classmethod
    def from_dict(cls, d):
        return cls(
            transitions=[Transition(**t) for t in d["transitions"]],
        )

    async def filterify(self, ctx, *srcs):
        # xfade requires all clips to start from 0 timebase
        srcs = [await ResetTimebase().filterify(ctx, src) for src in srcs]

        if len(self.transitions) + 1 != len(srcs):
            raise RuntimeError(
                f"concat_xfade given {len(srcs)} sources but expects {len(self.transitions) + 1} sources (because there are {len(self.transitions)} transitions defined"
            )

        left = srcs[0]
        for transition, right in zip(self.transitions, srcs[1:]):
            left = await self._concat(left, right, transition)

        return left

    async def _concat(self, left, right, transition):
        if transition.duration < 0.00001:
            strm = ffmpeg.filter(
                [left.strm, right.strm],
                "concat",
            )
        else:
            strm = ffmpeg.filter(
                [left.strm, right.strm],
                "xfade",
                transition=transition.effect,
                duration=transition.duration,
                offset=await left.actual_duration.get() - transition.duration,
            )

        async def total_duration():
            return (
                await left.actual_duration.get()
                + await right.actual_duration.get()
                - transition.duration
            )

        return Source(
            strm=strm,
            actual_duration=Lazy(total_duration),
            kind="video",
        )
