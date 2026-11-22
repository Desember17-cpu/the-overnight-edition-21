#!/usr/bin/env python3
"""Hand-in entry point for THE OVERNIGHT EDITION, round 5.

The finished page already sits next to this file as entry.png
(rendered locally by draw.py). At delivery time this program simply
carries that PNG into whichever output directory the runner names
through the MAKEFUN_OUTPUT_DIR environment variable, falling back to
/output when the variable is not set.
"""

import os
import shutil
import sys

PAGE_FILE = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, PAGE_FILE)
    if not os.path.isfile(source):
        print("missing rendered page:", source, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, PAGE_FILE)
    shutil.copyfile(source, target)
    print("delivered %s -> %s" % (PAGE_FILE, target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
