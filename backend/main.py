"""Main application entry point for the MCP agent."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from .tools import browser, command_exec, file_ops, gui_ops
from .tools.browser import browse, BrowseReq
from .tools.command_exec import run_command, RunCmd
from .tools.file_ops import read_file, write_file, ReadReq, WriteReq
from .tools.gui_ops import click, type_text, ClickPayload, TypeTextPayload
from .auth import get_api_key


load_dotenv()

app = FastAPI()

app.include_router(browser.router)
app.include_router(command_exec.router)
app.include_router(file_ops.router)
app.include_router(gui_ops.router)


@app.post("/")
async def mcp_rpc(request: Request) -> JSONResponse:
    """Dispatch JSON-RPC calls to the appropriate tool functions."""

    rpc = await request.json()
    method = rpc.get("method")
    params = rpc.get("params", {})
    req_id = rpc.get("id")

    try:
        api_key = get_api_key(request.headers.get("X-API-KEY"))

        if method == "run_command":
            payload = RunCmd(**params)
            result = run_command(payload, api_key=api_key)
        elif method == "read_file":
            payload = ReadReq(**params)
            result = read_file(payload, api_key=api_key)
        elif method == "write_file":
            payload = WriteReq(**params)
            result = write_file(payload, api_key=api_key)
        elif method == "click":
            payload = ClickPayload(**params)
            result = click(payload, api_key=api_key)
        elif method == "type_text":
            payload = TypeTextPayload(**params)
            result = type_text(payload, api_key=api_key)
        elif method == "browse":
            payload = BrowseReq(**params)
            result = await browse(payload, api_key=api_key)
        else:
            raise ValueError(f"Unknown method {method}")

        return JSONResponse({"jsonrpc": "2.0", "result": result, "id": req_id})

    except Exception as exc:  # pragma: no cover - best effort error report
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": str(exc)},
                "id": req_id,
            }
        )


@app.get("/health")
def health() -> dict[str, str]:
    """Simple healthcheck endpoint."""

    return {"status": "ok"}


__all__ = ["app"]

