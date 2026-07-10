from dataclasses import dataclass, replace
from typing import Optional

import ffmpeg

@dataclass
class Split:
    branch_names: list[str]
    split_main_branch: bool = False # make an extra split that allows adding more filters in the chain after this one

    @staticmethod
    def ref():
        return 'split'

    async def filterify(self, ctx, source):
        n = len(self.branch_names)
        strm = source.strm

        if self.split_main_branch:
            n += 1

        split = strm.filter_multi_output('split', n)

        branches = {name: split.stream(i) for i, name in enumerate(self.branch_names)}

        if self.split_main_branch:
            strm = split.stream(n-1)

        return replace(source, strm=strm, branches=branches)
