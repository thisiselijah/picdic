# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Practice environment for IC design contests: gate-level synthesis and
physical design (RTL → gate-level netlist → GDSII), with past exam problems
kept as separate, self-contained directories.

## Layout

- `exams/<year>-<title>/` — one directory per past exam. Each contains
  `spec/` (problem statement), `rtl/`, `tb/`, `constraints/*.sdc`, plus
  `sim/`, `synth/`, `pnr/`, `reports/` as run/output dirs. New exams are
  created from `exams/_template/` via `uv run scripts/new_exam.py <year> "<title>"`
  — don't hand-roll a new exam directory, use the script so the naming and
  subdirs stay consistent.
- `common/flow/opensource/` — reusable, generic (not exam-specific) sim/synth/PnR
  scripts for the open-source toolchain. The Python script is the entry
  point in each case; it shells out to the actual EDA tool (Tcl scripts are
  implementation detail, not meant to be invoked directly):
  - `sim/verilator/run_sim.py <exam_dir> [--top TB_TOP] [--wave]` compiles+runs
    all RTL/TB under the exam with Verilator (`--trace-fst`), inferring
    `--top` when the exam has exactly one testbench file, and outputs to
    `<exam_dir>/sim/` (gitignored). `--wave` opens the dump in Surfer.
  - `synth/yosys/run_synth.py <exam_dir> <top> --liberty <path>` drives
    `synth.tcl` (reads all `.v`/`.sv` under `<exam_dir>/rtl/`).
  - `pnr/openroad/run_pnr.py <exam_dir> <top>` wraps the OpenROAD Docker
    flow, invoking `run_pnr.tcl` inside the container, which reads per-exam
    `pnr/config.tcl` (utilization, placement density, CTS buffer, LEF/LIB
    paths).
- `common/flow/commercial/` — equivalent templates for Synopsys Design
  Compiler (`synth/dc/run_dc.tcl`) and Cadence Innovus (`pnr/innovus/run_innovus.tcl`).
  These require a licensed local install; they are not runnable in this
  environment as-is and expect site-specific library/PDK env vars
  (`TARGET_LIBS`, `MMMC_FILE`, `LEF_FILES`, etc.) to be set before invocation.
- `env/setup.sh` — the one shell script in the repo: installs the open-source
  toolchain via Homebrew (yosys, magic, ngspice, klayout, surfer, uv), runs
  `uv sync` for the Python env, and prints the `docker pull` command for
  OpenROAD (not run automatically — it's a multi-GB image). Verilator is
  assumed already installed and is used for simulation.
- `pyproject.toml` / `.venv/` — uv-managed Python dev environment. Every
  tool-call script (`scripts/new_exam.py`, and everything under
  `common/flow/opensource/`) is Python, invoked via `uv run <script>`, not
  executed directly — this guarantees the pinned interpreter/deps regardless
  of what `python3` resolves to on the host shell.

## Toolchain

Open-source flow (primary, runnable locally):
- **Synthesis:** yosys
- **Place & route:** OpenROAD, run via Docker (`openroad/orfs` image) — no
  native macOS build is used here
- **Layout/DRC/GDS viewing:** magic, klayout
- **Simulation:** verilator (already installed)
- **Waveform viewing:** Surfer (`.vcd`/`.fst` output from verilator)

Commercial flow (Synopsys/Cadence): script templates only, under
`common/flow/commercial/`. Requires the user's own tool install and license —
do not attempt to install or invoke these tools directly.

PDKs and vendor standard-cell libraries (`*.lib`, `*.lef`, `*.gds`, and
anything under `common/pdk/`) are gitignored — they're fetched/placed locally
per exam, not committed.

## Common commands

```
env/setup.sh                                        # install EDA tools + uv sync
uv run scripts/new_exam.py <year> "<title>"          # scaffold exams/<year>-<title>/
uv run common/flow/opensource/sim/verilator/run_sim.py exams/<year>-<title> [--top TB_TOP] [--wave]
uv run common/flow/opensource/synth/yosys/run_synth.py exams/<year>-<title> <top> --liberty <path>
uv run common/flow/opensource/pnr/openroad/run_pnr.py exams/<year>-<title> <top>
```
