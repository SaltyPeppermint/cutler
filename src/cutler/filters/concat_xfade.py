from dataclasses import dataclass, replace

import ffmpeg

from cutler.data import Source
from cutler.filters.reset_timebase import ResetTimebase
from cutler.lazy import Lazy

@dataclass
class Transition:
    effect: str = 'fade'
    duration: float = 0

@dataclass
class ConcatXFade:
    transitions: list[Transition]

    @staticmethod
    def ref():
        return 'concat_xfade'

    @classmethod
    def from_dict(cls, d):
        return cls(
            transitions=[Transition(**t) for t in d['transitions']],
        )

    async def filterify(self, ctx, *srcs):
        # xfade requires all clips to start from 0 timebase
        srcs = [await ResetTimebase().filterify(ctx, src) for src in srcs]

        if len(self.transitions) + 1 != len(srcs):
            raise RuntimeErrror(f'concat_xfade given {len(srcs)} sources but expects {len(self.transitions) + 1} sources (because there are {len(self.transitions)} transitions defined')

        l = srcs[0]
        for transition, r in zip(self.transitions, srcs[1:]):
            l = await self._concat(l, r, transition)

        return l

    async def _concat(self, l, r, transition):
        if transition.duration < 0.00001:
            strm = ffmpeg.filter(
                [l.strm, r.strm],
                'concat',
            )
        else:
            strm = ffmpeg.filter(
                [l.strm, r.strm],
                'xfade',
                transition=transition.effect,
                duration=transition.duration,
                offset=await l.actual_duration.get() - transition.duration,
            )

        async def total_duration():
            return await l.actual_duration.get() + await r.actual_duration.get() - transition.duration

        return Source(
            strm=strm,
            actual_duration=Lazy(total_duration),
            kind='video',
        )
