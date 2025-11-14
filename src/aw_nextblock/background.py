"""Helpers for running the watcher in the background."""
from __future__ import annotations

import os
import subprocess
import sys


def _build_watcher_command() -> list[str]:
    """Return the command that runs the watcher CLI entry."""
    if getattr(sys, "frozen", False):
        # Frozen/pyinstaller executables re-invoke themselves.
        return [sys.executable, "watcher"]
    # For standard python environments execute the module directly.
    return [sys.executable, "-m", "aw_nextblock", "watcher"]


def launch_watcher_background() -> int:
    """Start the watcher in a detached subprocess and return its PID."""
    cmd = _build_watcher_command()
    popen_kwargs = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }

    if os.name == "nt":
        creationflags = 0
        # Detach completely so the watcher does not hold the console open.
        creationflags |= getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
        creationflags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
        popen_kwargs["creationflags"] = creationflags
    else:
        # Start a new session so the watcher is fully detached from the shell.
        popen_kwargs["start_new_session"] = True

    process = subprocess.Popen(cmd, **popen_kwargs)
    return process.pid
