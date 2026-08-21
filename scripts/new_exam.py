#!/usr/bin/env python3
"""Scaffold a new exam directory from exams/_template.

Usage:
    uv run scripts/new_exam.py <year> "<title>"

Example:
    uv run scripts/new_exam.py 2024 "low-power-adder"
    # -> exams/2024-low-power-adder/
"""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("year")
    parser.add_argument("title")
    args = parser.parse_args()

    title = args.title.replace(" ", "-")
    dest = ROOT / "exams" / f"{args.year}-{title}"

    if dest.exists():
        sys.exit(f"error: {dest} already exists")

    shutil.copytree(ROOT / "exams" / "_template", dest)

    readme = dest / "README.md"
    text = readme.read_text()
    text = text.replace("<Exam Title>", title).replace("<year>", args.year)
    readme.write_text(text)

    print(f"created {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
