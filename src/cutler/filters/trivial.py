from dataclasses import dataclass, replace
from typing import Optional

import ffmpeg

@dataclass
class GetAudio:
    @staticmethod
    def ref():
        return 'get_audio'

    async def filterify(self, source):
        return replace(source, strm=source.strm.audio, kind='audio')

@dataclass
class GetVideo:
    @staticmethod
    def ref():
        return 'get_video'

    async def filterify(self, source):
        return replace(source, strm=source.strm.video, kind='video')
