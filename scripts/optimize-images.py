#!/usr/bin/env python3
"""Generates responsive image variants using macOS sips."""

import os
import subprocess
from pathlib import Path

SRC_DIR = Path(__file__).parent.parent / "assets" / "images"
OUT_DIR = SRC_DIR / "optimized"
WIDTHS = [400, 800, 1200]
QUALITY = 80

OUT_DIR.mkdir(exist_ok=True)

sources = [f for f in SRC_DIR.glob("*.jpg") if not f.stem.endswith(("w",))]

for src in sorted(sources):
    for w in WIDTHS:
        out = OUT_DIR / f"{src.stem}-{w}w.jpg"
        if out.exists():
            print(f"  skip {out.name}")
            continue
        subprocess.run([
            "sips",
            "--resampleWidth", str(w),
            "-s", "format", "jpeg",
            "-s", "formatOptions", str(QUALITY),
            str(src),
            "--out", str(out),
        ], check=True, capture_output=True)
        orig_kb = src.stat().st_size // 1024
        new_kb = out.stat().st_size // 1024
        print(f"  {src.name} → {out.name}  ({orig_kb}KB → {new_kb}KB)")

print("Done.")
