from dataclasses import dataclass

import ffmpeg

from cutler.data import Source

@dataclass
class ReadClip:
    filename: str
    looped: bool = False

    @staticmethod
    def ref():
        return 'read_clip'

    def filterify(self):
        strm = ffmpeg.input(self.filename)
        if self.looped:
            raise RuntimeError('not implemented (FIXME: pass loop arg to ffmpeg for this input)')

        try:
            # TODO: make this probe be lazy
            probe = ffmpeg.probe(self.filename)
        except ffmpeg.Error as e:
            sys.stderr.write(e.stderr.decode('utf-8'))
            raise

        return Source(
            strm=strm,
            actual_duration=float(probe['format']['duration']),
        )

