#!/usr/bin/env python3
"""Delivery entry point for the challenger-b4 news page.

The artwork already exists as entry.png alongside this file (rendered
by draw.py). All this program does at hand-in time is carry that file
into the output directory the runner designates.
"""

import os
import shutil
from pathlib import Path

SOURCE_NAME = "entry.png"
FALLBACK_TARGET = "/output"


def deliver() -> Path:
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", FALLBACK_TARGET))
    target_dir.mkdir(parents=True, exist_ok=True)

    origin = Path(__file__).resolve().parent / SOURCE_NAME
    destination = target_dir / SOURCE_NAME
    shutil.copyfile(origin, destination)
    return destination


if __name__ == "__main__":
    placed = deliver()
    print(f"delivered {SOURCE_NAME} -> {placed}")
