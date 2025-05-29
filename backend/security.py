"""Security related helpers for command and file access control."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


# Whitelist of allowed shell commands. Only the command name (first token)
# is checked. Arguments are not validated here.
ALLOWED_COMMANDS: list[str] = [
    "ls",
    "cat",
    "echo",
    "grep",
    "pwd",
]

# Base directories allowed for file operations. Any path resolved under one of
# these directories will be considered safe.
ALLOWED_BASE_DIRS: list[Path] = [
    Path("/workspace"),
    Path("/tmp"),
]


def _normalize_path(path: str) -> Path:
    """Return the absolute resolved ``Path`` for ``path``."""

    return Path(path).expanduser().resolve()


def _is_relative_to(path: Path, *parents: Iterable[Path]) -> bool:
    """Backport of ``Path.is_relative_to`` for Python <3.9."""

    for parent in parents:
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            continue
    return False


def is_cmd_allowed(cmd: list[str]) -> bool:
    """Return ``True`` if the command is permitted to run.

    Parameters
    ----------
    cmd:
        Tokenized command where ``cmd[0]`` is the executable name.
    """

    if not cmd:
        return False
    executable = Path(cmd[0]).name
    return executable in ALLOWED_COMMANDS


def is_path_allowed(path: str) -> bool:
    """Return ``True`` if ``path`` is within an allowed directory."""

    target = _normalize_path(path)
    return _is_relative_to(target, *ALLOWED_BASE_DIRS)


__all__ = [
    "is_cmd_allowed",
    "is_path_allowed",
    "ALLOWED_COMMANDS",
    "ALLOWED_BASE_DIRS",
]

