import logging.config
import asyncio

import typer
from loguru import logger

from macos_lyric.service import universal_search
from macos_lyric.utility import get_info

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
    }
)


async def run(app: bool, debug: bool):  # pragma: no cover
    {True: logger.enable, False: logger.disable}[debug]("macos_lyric")

    if not debug:
        logger.disable("macos_lyric")
        logger.disable("__main__")

    media_info = get_info(app)
    if media_info is None:
        return

    songs = await universal_search(media_info.name, media_info.artists)
    logger.debug(f"Found {len(songs)} songs:")
    for song in songs:
        logger.debug(f"{song.source}: {song.artists} - {song.title}")
    for song in songs:
        line: str = song.anchor(media_info.position)
        if line or line == "":
            logger.debug(f"found anchor {media_info.position} in {song.source}: {song.artists} - {song.title}")
            print(line)
            break


def main(
        app: str = typer.Option(default="Spotify", help="Application to track"),
        debug: bool = typer.Option(
            default=False, is_flag=True, help="To show debug messages or not"
        ),
):
    asyncio.run(run(app, debug))


if __name__ == "__main__":  # pragma: no cover
    typer.run(main)
