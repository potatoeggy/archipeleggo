import base64
import contextlib
from dataclasses import dataclass
import os
from pathlib import Path
import re
from typing import cast


from ...config import CONFIG_ISLAND_MUSIC_CACHE_PATH
import eyed3
import eyed3.id3
import eyed3.core
from eyed3.mp3 import Mp3AudioFile


@dataclass
class MusicLyric:
    timestamp: float
    text: str


@dataclass
class MusicFile:
    title: str | None
    artist: str | None
    album: str | None
    duration: float
    path: str
    art_base64: str | None  # base64 encoded image
    lyrics: list[MusicLyric] | None


def search_cache_music_mp3s() -> list[MusicFile]:
    music_files: list[MusicFile] = []
    for mp3 in Path(CONFIG_ISLAND_MUSIC_CACHE_PATH).rglob("*.mp3"):
        with open(os.devnull, "w") as null:
            with contextlib.redirect_stdout(null):
                with contextlib.redirect_stderr(null):
                    audiofile = cast(Mp3AudioFile | None, eyed3.load(mp3))

        if audiofile is None or audiofile.tag is None:
            continue

        # read external lrc file
        try:
            lrc_file = mp3.with_suffix(".lrc")
            with open(lrc_file, "r") as f:
                lyrics: list[MusicLyric] | None = []
                for line in f:
                    # [00:00.00] text
                    try:
                        ts_end_index = line.index("]")
                        ts = line[1:ts_end_index]
                        ts_seconds = sum(
                            x * int(t)
                            for x, t in zip(
                                [0.001, 1, 60], reversed(re.split(r":|\.", ts))
                            )
                        )
                        lyric = line[ts_end_index + 1 :].strip()
                        if lyric and not lyric.isspace():
                            lyrics.append(MusicLyric(timestamp=ts_seconds, text=lyric))
                    except IndexError:
                        # expected if newline or badly formatted LRC
                        pass
                    except ValueError:
                        # current line does not have a timestamp
                        pass
        except IOError:
            lyrics = None

        art_base64 = next(iter(audiofile.tag.images), None)
        if art_base64 is not None:
            art_base64 = base64.b64encode(art_base64.image_data).decode("utf-8")

        music_files.append(
            MusicFile(
                title=audiofile.tag.title,
                artist=audiofile.tag.artist,
                album=audiofile.tag.album,
                path=str(mp3.relative_to(CONFIG_ISLAND_MUSIC_CACHE_PATH)),
                duration=audiofile.info.time_secs,
                art_base64=art_base64,
                lyrics=lyrics,
            )
        )

    return music_files


CACHE_MUSIC_FILES: list[MusicFile] = search_cache_music_mp3s()
