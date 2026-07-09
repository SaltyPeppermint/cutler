from dataclasses import dataclass, replace

import ffmpeg

from cutler.data import Source
from cutler.filters.reset_timebase import ResetTimebase

@dataclass
class ConcatAudioFade:
    transition_durations: list[float]

    @staticmethod
    def ref():
        return 'concat_audio_fade'

    def filterify(self, *srcs):
        # TODO: this repeats code from `concat_xfade`, find a way to merge it
        # crossfade requires all clips to start from 0 timebase
        srcs = list(map(ResetTimebase().filterify, srcs))

        if len(self.transition_durations) + 1 != len(srcs):
            raise RuntimeErrror(f'concat_audio_fade given {len(srcs)} sources but expects {len(self.transition_durations) + 1} sources (because there are {len(self.transition_durations)} transitions defined')

        l = srcs[0]
        for duration, r in zip(self.transition_durations, srcs[1:]):
            l = self._concat(l, r, duration)

        return l

    def _concat(self, l, r, duration):
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

        return Source(
            strm=strm,
            actual_duration=l.actual_duration + r.actual_duration - duration,
            kind='audio',
        )

