from pathlib import Path
from fastapi import APIRouter, HTTPException


from ...utils import create_file_response

from ...config import CONFIG_ISLAND_MUSIC_CACHE_PATH

from .cache_player import CACHE_MUSIC_FILES, MusicFile


router = APIRouter(prefix="/music")

@router.get("/cache/files", response_model=list[MusicFile])
def get_music_cache_files() -> list[MusicFile]:
    return CACHE_MUSIC_FILES

@router.get("/cache/files/{filename}")
def get_music_cache_file(filename: str):
    if filename.startswith("."):
        raise HTTPException(403, "You cannot access hidden files")

    abspath = Path(CONFIG_ISLAND_MUSIC_CACHE_PATH) / filename

    if not abspath.exists():
        raise HTTPException(404, "File not found")

    return create_file_response(path=abspath, filename=filename, media_type="audio/mp3")
