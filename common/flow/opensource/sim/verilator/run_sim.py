#!/usr/bin/env python3
"""Compile + run an exam's testbench with Verilator, dumping an FST waveform,
and optionally open it in Surfer.

Usage:
    uv run common/flow/opensource/sim/verilator/run_sim.py <exam_dir> [--top TB_TOP] [--wave]

Reads all *.v/*.sv under <exam_dir>/rtl and <exam_dir>/tb. Build artifacts
and the waveform dump are written to <exam_dir>/sim/ (gitignored).
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

SRC_EXTS = ("*.v", "*.sv")


def find_sources(directory: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in SRC_EXTS:
        files.extend(sorted(directory.glob(pattern)))
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exam_dir", type=Path, help="e.g. exams/2024-low-power-adder")
    parser.add_argument("--top", help="testbench top module (inferred if tb/ has one file)")
    parser.add_argument("--wave", action="store_true", help="open the waveform in Surfer after running")
    args = parser.parse_args()

    exam_dir = args.exam_dir.resolve()
    rtl_dir = exam_dir / "rtl"
    tb_dir = exam_dir / "tb"
    sim_dir = exam_dir / "sim"
    sim_dir.mkdir(parents=True, exist_ok=True)

    rtl_files = find_sources(rtl_dir)
    tb_files = find_sources(tb_dir)

    if not tb_files:
        sys.exit(f"error: no testbench files found in {tb_dir}")

    tb_top = args.top
    if not tb_top:
        if len(tb_files) != 1:
            sys.exit(f"error: multiple files in {tb_dir}, pass --top explicitly")
        tb_top = re.sub(r"\.(v|sv)$", "", tb_files[0].name)
        print(f"inferred tb_top: {tb_top}")

    obj_dir = sim_dir / "obj_dir"
    cmd = [
        "verilator", "--binary", "--trace-fst", "--timing", "-Wno-fatal",
        "--top-module", tb_top,
        "-I" + str(rtl_dir),
        *[str(f) for f in rtl_files],
        *[str(f) for f in tb_files],
        "--Mdir", str(obj_dir),
    ]
    print("+", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        return result.returncode

    binary = obj_dir / f"V{tb_top}"
    print("+", binary)
    result = subprocess.run([str(binary)], cwd=sim_dir)
    if result.returncode != 0:
        return result.returncode

    dumps = sorted(sim_dir.glob("*.fst"))
    dump = dumps[0] if dumps else None
    print(f"waveform: {dump}")

    if args.wave and dump:
        subprocess.run(["surfer", str(dump)])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
