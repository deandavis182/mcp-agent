"""Main application entry point for the MCP agent."""

from __future__ import annotations

from fastapi import FastAPI
from dotenv import load_dotenv

from .tools import browser, command_exec, file_ops, gui_ops


load_dotenv()

app = FastAPI()

app.include_router(browser.router)
app.include_router(command_exec.router)
app.include_router(file_ops.router)
app.include_router(gui_ops.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple healthcheck endpoint."""

    return {"status": "ok"}


__all__ = ["app"]

