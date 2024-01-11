import logging.config
import asyncio
import os
from typing import List, Tuple

from diskcache import FanoutCache
from loguru import logger

from macos_lyric import Song
from macos_lyric.service.misc import (lyricsify_music_search,
                                      megalobiz_music_search,
                                      rclyricsband_music_search,
                                      rentanadviser_music_search)
from macos_lyric.service.netease import netease_music_search

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
    }
)

CACHE = os.path.join(os.path.expanduser("~"), ".cache/macos-lyric")

if not os.path.exists(CACHE):
    os.mkdir(CACHE)

cache = FanoutCache(CACHE, timeout=2)

LOCK = "/tmp/macos-lyric"

if not os.path.exists(LOCK):
    os.mkdir(LOCK)


async def universal_search(title: str, artists: str) -> List[Song]:  # pragma: no cover
    songs_cached = cache.get(f"{artists}-{title}")
    if songs_cached:
        return songs_cached

    lockfile = f"{artists}-{title}.lock"
    if os.path.exists(os.path.join(LOCK, lockfile)):
        logger.debug("Searching...")
        return []
    else:
        open(os.path.join(LOCK, lockfile), 'a').close()

    logger.debug("Searching...")

    tasks = [
        netease_music_search(title, artists),
        # rentanadviser_music_search(title, artists),
        # megalobiz_music_search(title, artists),
        # lyricsify_music_search(title, artists),
        # rclyricsband_music_search(title, artists),
    ]

    results = await asyncio.gather(*tasks)

    songs: List[Tuple[int, Song]] = []
    for i, sons_from_service in enumerate(results):
        songs.extend((-i, s) for s in sons_from_service)

    songs_sorted = [s[1] for s in songs]

    if os.path.exists(os.path.join(LOCK, lockfile)):
        os.remove(os.path.join(LOCK, lockfile))

    cache.set(f"{artists}-{title}", songs_sorted, tag="lyric", expire=7776000)

    return songs_sorted
