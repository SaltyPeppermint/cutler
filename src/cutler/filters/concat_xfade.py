from dataclasses import dataclass, replace

import ffmpeg

@dataclass
class Transition:
    effect: str = 'fade'
    duration: float = 0

@dataclass
class ConcatXFade:
    transitions: list[Transition]

    def filterify(self, *srcs):
        # xfade requires all clips to start from 0 timebase
        srcs = map(srcs, ResetTimebase().filterify)

        if len(self.transitions) + 1 != len(srcs):
            raise RuntimeErrror(f'concat_xfade given {len(srcs)} sources but expects {len(self.transitions) + 1} sources (because there are {len(self.transitions)} transitions defined')

        l = srcs[0]
        for transition, r in zip(self.transitions, srcs[1:]):
            l = self._concat(l, r, transition)

        return l

    def _concat(self, l, r, transition):
        return Source(
            strm=ffmpeg.filter(
                [l.strm, r.strm],
                'xfade',
                transition=transition.effect,
                duration=transition.duration,
                offset=l.actual_duration - transition.duration,
            ),
            actual_duration=l.actual_duration + r.actual_duration - l.transition.duration,
        )
