"""Helpers for executing shell commands through the API."""

from __future__ import annotations

import subprocess
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..auth import get_api_key
from ..logger import log_invocation
from ..security import is_cmd_allowed


class RunCmd(BaseModel):
    """Model representing a command to execute."""

    cmd: list[str]


router = APIRouter()


@router.post("/run_command")
def run_command(payload: RunCmd, api_key: str = Depends(get_api_key)) -> dict[str, Any]:
    """Execute a whitelisted shell command and return its output."""

    log_invocation("/run_command", payload.dict(), api_key)

    if not is_cmd_allowed(payload.cmd):
        raise HTTPException(status_code=400, detail="Command not allowed")

    try:
        output = subprocess.check_output(
            payload.cmd, stderr=subprocess.STDOUT, text=True
        )
        return {"output": output}
    except subprocess.CalledProcessError as exc:
        return {"error": exc.output}


__all__ = ["router", "RunCmd"]

