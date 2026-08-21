#!/usr/bin/env python3
"""Run Yosys gate-level synthesis for an exam.

Usage:
    uv run common/flow/opensource/synth/yosys/run_synth.py <exam_dir> <top> --liberty <path>
"""
import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SYNTH_TCL = SCRIPT_DIR / "synth.tcl"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exam_dir", type=Path, help="e.g. exams/2024-low-power-adder")
    parser.add_argument("top", help="top module name")
    parser.add_argument("--liberty", required=True, type=Path, help="path to tech .lib file")
    args = parser.parse_args()

    exam_dir = args.exam_dir.resolve()
    rtl_dir = exam_dir / "rtl"
    out_dir = exam_dir / "synth"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not rtl_dir.is_dir():
        sys.exit(f"error: {rtl_dir} does not exist")
    if not args.liberty.is_file():
        sys.exit(f"error: liberty file not found: {args.liberty}")

    cmd = [
        "yosys", "-c", str(SYNTH_TCL),
        "--", args.top, str(rtl_dir), str(args.liberty.resolve()), str(out_dir),
    ]
    print("+", " ".join(cmd))
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
