# authentication utilities

from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os


def get_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-KEY"),
) -> str:
    """Validate the API key sent in request headers.

    Loads environment variables using ``python-dotenv`` and compares the
    ``X-API-KEY`` header against the ``MCP_API_KEY`` environment variable.

    Parameters
    ----------
    x_api_key: str | None
        The value of the ``X-API-KEY`` header provided by the client.

    Returns
    -------
    str
        The validated API key.

    Raises
    ------
    HTTPException
        If the header is missing or does not match the expected value.
    """

    load_dotenv()
    expected_key = os.getenv("MCP_API_KEY")

    if not expected_key or x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

    return x_api_key

