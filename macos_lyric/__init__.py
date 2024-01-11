import html
from dataclasses import dataclass
from typing import List, Optional, Tuple
from loguru import logger

import regex as re

from macos_lyric.utility import search_intervals


@dataclass
class Song:

    title: str
    artists: str
    target_title: str
    target_artists: str
    lyric: str
    source: str
    lines: Optional[List[Tuple[float, str]]] = None
    intervals: Optional[List[float]] = None

    def __post_init__(self):

        lyric = self.lyric
        lyric = html.unescape(lyric)

        self.lines = []
        self.intervals = []
        for line in lyric.split("\n"):
            info, *words = line.rsplit("]", 1)
            timestamp = re.search(r"\[([0-9]+):([0-9]+)\.([0-9]+)\]", info + "]")
            if not timestamp:
                continue
            minute, second, subsecond = (
                timestamp.group(1),
                timestamp.group(2),
                timestamp.group(3),
            )
            curr_stamp = int(minute) * 60 + int(second) + \
                int(subsecond) / (10**len(subsecond))
            self.lines.append((curr_stamp, "".join(words)))
            self.intervals.append(curr_stamp)

    def anchor(self, timestamp: float) -> Optional[str]:
        """Find current timestamp for this song.

        Parameters
        ----------
        timestamp : float
            Current timestamp

        Returns
        -------
        Optional[str]
            A line or None

        Examples
        --------
        >>> song = Song("Hello", "Adele", "Hello", "Adele", "[01:12.34]Hello")
        >>> song.anchor(60)
        'Hello'
        >>> song.anchor(120)
        'Hello'
        >>> song = Song("Hello", "Adele", "Hello", "Adele", "")
        >>> song.anchor(10) is None
        True
        """
        if not self.intervals or not self.lines:
            return None

        idx = search_intervals(self.intervals, timestamp)
        logger.debug(f"idx: {idx}")

        if idx != -1:
          logger.debug(f"got: {self.lines[idx][-1].strip()}")
          return self.lines[idx][-1].strip()

        return None
