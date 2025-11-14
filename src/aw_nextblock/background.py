"""Helpers for running the watcher in the background."""
from __future__ import annotations

import asyncio
import multiprocessing

from .watcher import watcher_async


def _watcher_entry():
    """Entry point for the background watcher process."""
    asyncio.run(watcher_async())


def launch_watcher_background() -> int:
    """Start the watcher in a separate process and return its PID."""
    ctx = multiprocessing.get_context("spawn")
    process = ctx.Process(target=_watcher_entry, name="aw-nextblock-watcher")
    process.start()
    return process.pid
