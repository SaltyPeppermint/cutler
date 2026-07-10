from dataclasses import dataclass

import ffmpeg

from cutler.data import Source
from cutler.lazy import Lazy
from cutler.filters.reset_timebase import ResetTimebase


@dataclass
class ConcatAudioFade:
    transition_durations: list[float]

    @staticmethod
    def ref():
        return "concat_audio_fade"

    async def filterify(self, ctx, *srcs):
        # TODO: this repeats code from `concat_xfade`, find a way to merge it
        # crossfade requires all clips to start from 0 timebase
        srcs = [await ResetTimebase().filterify(ctx, src) for src in srcs]

        if len(self.transition_durations) + 1 != len(srcs):
            raise RuntimeError(
                f"concat_audio_fade given {len(srcs)} sources but expects {len(self.transition_durations) + 1} sources (because there are {len(self.transition_durations)} transitions defined"
            )

        left = srcs[0]
        for duration, right in zip(self.transition_durations, srcs[1:]):
            left = await self._concat(left, right, duration)

        return left

    async def _concat(self, left, right, duration):
        if duration < 0.00001:
            strm = ffmpeg.filter(
                [left.strm, right.strm],
                "concat",
                v=0,
                a=1,
            )
        else:
            strm = ffmpeg.filter(
                [left.strm, right.strm],
                "acrossfade",
                d=duration,
            )

        async def total_duration():
            return await left.actual_duration.get() + await right.actual_duration.get() - duration

        return Source(
            strm=strm,
            actual_duration=Lazy(total_duration),
            kind="audio",
        )
