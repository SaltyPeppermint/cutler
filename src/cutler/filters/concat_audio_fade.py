from dataclasses import dataclass, replace

import ffmpeg

from cutler.data import Source
from cutler.lazy import Lazy
from cutler.filters.reset_timebase import ResetTimebase

@dataclass
class ConcatAudioFade:
    transition_durations: list[float]

    @staticmethod
    def ref():
        return 'concat_audio_fade'

    async def filterify(self, ctx, *srcs):
        # TODO: this repeats code from `concat_xfade`, find a way to merge it
        # crossfade requires all clips to start from 0 timebase
        srcs = [await ResetTimebase().filterify(ctx, src) for src in srcs]

        if len(self.transition_durations) + 1 != len(srcs):
            raise RuntimeErrror(f'concat_audio_fade given {len(srcs)} sources but expects {len(self.transition_durations) + 1} sources (because there are {len(self.transition_durations)} transitions defined')

        l = srcs[0]
        for duration, r in zip(self.transition_durations, srcs[1:]):
            l = await self._concat(l, r, duration)

        return l

    async def _concat(self, l, r, duration):
        if duration < 0.00001:
            strm = ffmpeg.filter(
                [l.strm, r.strm],
                'concat',
                v=0, a=1,
            )
        else:
            strm = ffmpeg.filter(
                [l.strm, r.strm],
                'acrossfade',
                d=duration,
            )

        async def total_duration():
            return await l.actual_duration.get() + await r.actual_duration.get() - duration

        return Source(
            strm=strm,
            actual_duration=Lazy(total_duration),
            kind='audio',
        )

