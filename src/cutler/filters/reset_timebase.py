from dataclasses import dataclass, replace

import ffmpeg

@dataclass
class ResetTimebase:
    @staticmethod
    def ref():
        return 'reset_timebase'

    async def filterify(self, ctx, source):
        strm = source.strm

        if source.kind == 'video':
            strm = ffmpeg.filter(strm, 'settb', 'AVTB')
            strm = ffmpeg.filter(strm, 'setpts', 'PTS-STARTPTS')
        elif source.kind == 'audio':
            strm = ffmpeg.filter(strm, 'asettb', 'AVTB')
            strm = ffmpeg.filter(strm, 'asetpts', 'PTS-STARTPTS')
        else:
            raise RuntimeError('unclear if this is an audio or video stream: use the get_audio or get_video filter before this one')

        return replace(source, strm=strm)
