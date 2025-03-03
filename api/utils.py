import os
from pathlib import Path
from urllib.parse import quote

from fastapi.responses import StreamingResponse


def file_iterator(file_path: str | Path, chunk_size: int = 1024 * 4):
    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk


def create_file_response(
    *, path: str | Path, filename: str, media_type: str
) -> StreamingResponse:
    res = StreamingResponse(
        file_iterator(path),
        media_type=media_type,
    )

    # work around https://github.com/encode/starlette/pull/1163
    res.raw_headers.append(
        (
            b"Content-Disposition",
            f"attachment; filename*=utf-8''{quote(filename)}".encode("latin-1"),
        )
    )
    return res


def getenv_or_raise(key: str) -> str:
    return assert_not_none(os.getenv(key), key)


def getenv_or[T](key: str, default: T) -> str | T:
    return os.getenv(key) or default


def assert_not_none[T](value: T | None, value_name: str | None = None) -> T:
    if value is None:
        raise ValueError(f"{value_name or 'Value'} is None")
    return value
