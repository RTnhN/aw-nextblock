"""Module entry point used by both CLI and frozen binaries."""

import multiprocessing

from aw_nextblock.cli import cli


def main() -> None:
    """Entrypoint that ensures multiprocessing works when frozen."""
    multiprocessing.freeze_support()
    cli()


if __name__ == "__main__":
    main()
