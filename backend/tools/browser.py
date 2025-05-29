"""Browser automation helpers using Playwright."""

from __future__ import annotations

import base64
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from playwright.async_api import async_playwright

from ..auth import get_api_key
from ..logger import log_invocation


class BrowseReq(BaseModel):
    """Request model for the ``/browse`` endpoint."""

    url: str
    click_selector: str | None = None
    screenshot: bool = False


router = APIRouter()


@router.post("/browse")
async def browse(
    payload: BrowseReq, api_key: str = Depends(get_api_key)
) -> dict[str, Any]:
    """Open a URL, optionally click an element, and return a screenshot."""

    log_invocation("/browse", payload.dict(), api_key)

    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(payload.url)

            if payload.click_selector:
                await page.click(payload.click_selector)

            result: dict[str, Any] = {"status": "success"}
            if payload.screenshot:
                data = await page.screenshot()
                result["screenshot"] = base64.b64encode(data).decode()

            await context.close()
            await browser.close()
            return result
    except Exception as exc:  # pragma: no cover - best effort
        return {"status": "failure", "error": str(exc)}


__all__ = ["router", "BrowseReq"]

