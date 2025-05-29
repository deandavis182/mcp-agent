"""Helpers for reading and writing files through the API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..auth import get_api_key
from ..logger import log_invocation
from ..security import is_path_allowed


class ReadReq(BaseModel):
    """Request model for reading a file."""

    path: str


class WriteReq(BaseModel):
    """Request model for writing to a file."""

    path: str
    content: str


router = APIRouter()


@router.post("/read_file")
def read_file(payload: ReadReq, api_key: str = Depends(get_api_key)) -> dict[str, str]:
    """Return the contents of a permitted file."""

    log_invocation("/read_file", payload.dict(), api_key)

    if not is_path_allowed(payload.path):
        raise HTTPException(status_code=400, detail="File path not allowed")

    try:
        with open(payload.path, "r") as fh:
            content = fh.read()
    except OSError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {"content": content}


@router.post("/write_file")
def write_file(payload: WriteReq, api_key: str = Depends(get_api_key)) -> dict[str, str]:
    """Write content to a permitted file."""

    log_invocation("/write_file", payload.dict(), api_key)

    if not is_path_allowed(payload.path):
        raise HTTPException(status_code=400, detail="File path not allowed")

    try:
        with open(payload.path, "w") as fh:
            fh.write(payload.content)
    except OSError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {"status": "ok"}


__all__ = ["router", "ReadReq", "WriteReq"]
