#!/usr/bin/env python3
"""Run OpenROAD place-and-route for an exam via the ORFS Docker image.

Usage:
    uv run common/flow/opensource/pnr/openroad/run_pnr.py <exam_dir> <top>

Prerequisites:
    docker pull openroad/orfs:latest

Expects <exam_dir>/synth/<top>_netlist.v, <exam_dir>/constraints/*.sdc, and
<exam_dir>/pnr/config.tcl (see exams/_template/pnr/config.tcl).
"""
import argparse
import subprocess
import sys
from pathlib import Path

IMAGE = "openroad/orfs:latest"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exam_dir", type=Path, help="e.g. exams/2024-low-power-adder")
    parser.add_argument("top", help="top module name")
    args = parser.parse_args()

    exam_dir = args.exam_dir.resolve()
    if not exam_dir.is_dir():
        sys.exit(f"error: {exam_dir} does not exist")

    cmd = [
        "docker", "run", "--rm", "-it",
        "-v", f"{exam_dir}:/workspace",
        "-w", "/workspace",
        IMAGE,
        "bash", "-c", f"openroad -no_init -exit pnr/run_pnr.tcl -top {args.top}",
    ]
    print("+", " ".join(cmd))
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
