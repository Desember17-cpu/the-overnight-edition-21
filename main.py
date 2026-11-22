#!/usr/bin/env python3
"""Deliver the finished ONE PAGE WORLD page image to the grader.

The artwork itself is rendered ahead of time by draw.py and stored in this
folder as entry.png. At hand-in time all this program has to do is place a
copy of that file into whichever directory the MAKEFUN_OUTPUT_DIR
environment variable points at (falling back to /output).
"""

import os
from pathlib import Path

FALLBACK_DIR = "/output"
IMAGE_NAME = "entry.png"


def deliver() -> Path:
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR)
    target_dir.mkdir(parents=True, exist_ok=True)

    source = Path(__file__).resolve().parent / IMAGE_NAME
    destination = target_dir / IMAGE_NAME
    destination.write_bytes(source.read_bytes())
    return destination


if __name__ == "__main__":
    placed = deliver()
    print(f"entry image delivered to {placed} ({placed.stat().st_size} bytes)")
