"""GUI automation operations using pyautogui."""

from __future__ import annotations

from typing import Any

import pyautogui
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..auth import get_api_key
from ..logger import log_invocation


class ClickPayload(BaseModel):
    """Payload for the ``/click`` endpoint."""

    x: int
    y: int


class TypeTextPayload(BaseModel):
    """Payload for the ``/type_text`` endpoint."""

    text: str


router = APIRouter()


@router.post("/click")
def click(payload: ClickPayload, api_key: str = Depends(get_api_key)) -> dict[str, Any]:
    """Click at the specified screen coordinates."""

    log_invocation("/click", payload.dict(), api_key)

    try:
        pyautogui.click(payload.x, payload.y)
        return {"status": "success"}
    except Exception as exc:  # pragma: no cover - best effort for error reporting
        return {"status": "failure", "error": str(exc)}


@router.post("/type_text")
def type_text(
    payload: TypeTextPayload, api_key: str = Depends(get_api_key)
) -> dict[str, Any]:
    """Type the given text at the current cursor location."""

    log_invocation("/type_text", payload.dict(), api_key)

    try:
        pyautogui.write(payload.text)
        return {"status": "success"}
    except Exception as exc:  # pragma: no cover - best effort for error reporting
        return {"status": "failure", "error": str(exc)}


__all__ = ["router", "ClickPayload", "TypeTextPayload"]

