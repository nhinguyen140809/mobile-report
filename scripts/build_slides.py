#!/usr/bin/env python3
"""Build the Beamer slide deck (slides/main.tex) with the same TinyTeX toolchain
as the report. Run from anywhere: paths are resolved from this file's location.

Usage: python3 scripts/build_slides.py
Output: build/slides/slides.pdf, copied to ./slides.pdf at the repo root.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "slides" / "main.tex"
BUILD = ROOT / "build" / "slides"
PDF_OUT = ROOT / "slides.pdf"
LOG = BUILD / "main.log"


def main() -> int:
    if shutil.which("pdflatex") is None:
        sys.exit("pdflatex not found in PATH. See the 'Install compiler' section in README.md.")

    BUILD.mkdir(parents=True, exist_ok=True)
    if not SRC.exists():
        sys.exit(f"Missing {SRC}")

    # Two passes are enough: no bibliography / no cross references in the deck.
    for label in ("pass 1", "pass 2"):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(BUILD), str(SRC)],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"  {label}: {'OK' if result.returncode == 0 else 'WARN'}")

    pdf = BUILD / "main.pdf"
    if not pdf.exists():
        if LOG.exists():
            for line in LOG.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("!"):
                    print(line)
        return 1

    shutil.copy(pdf, PDF_OUT)
    pages = re.findall(r"Output written on .*?\((\d+) pages", LOG.read_text(encoding="utf-8", errors="replace"))
    print(f"\nSlides: {PDF_OUT.name} ({pages[0] if pages else '?'} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
