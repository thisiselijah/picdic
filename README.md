# picdic — IC design contest practice

Practice environment for gate-level synthesis and physical design (RTL →
netlist → GDSII), organized by past contest problems.

## Layout

```
exams/<year>-<title>/   one directory per past exam (see exams/_template)
common/flow/            shared sim/synth/P&R tool-call scripts, open-source + commercial
env/setup.sh            installs the toolchain: EDA tools (Homebrew) + Python env (uv)
scripts/new_exam.py     scaffold a new exams/<year>-<title>/ from the template
pyproject.toml          uv-managed Python env; all tool-call scripts run via `uv run`
```

## Setup

```
env/setup.sh
```

Installs yosys, magic, ngspice, klayout, surfer, uv via Homebrew (Verilator is
assumed already installed for simulation), then `uv sync` to set up the
Python dev environment. OpenROAD runs via Docker
(`docker pull openroad/orfs:latest`) rather than a native build. Commercial
tools (Design Compiler, Innovus) require your own licensed install; only
script templates are provided under `common/flow/commercial/`.

Installing tools stays shell-based (`env/setup.sh`); every script that
actually drives a tool (scaffolding, sim, synth, P&R) is a Python script run
via `uv run`.

## Starting a new exam

```
uv run scripts/new_exam.py 2024 "low-power-adder"
# -> exams/2024-low-power-adder/
```

Fill in `spec/`, `rtl/`, `tb/`, `constraints/*.sdc`, then simulate, synthesize,
and place-and-route using the shared scripts in `common/flow/opensource/`.

## Simulating (Verilator + Surfer)

```
uv run common/flow/opensource/sim/verilator/run_sim.py exams/2024-low-power-adder --wave
```

Compiles all RTL/TB under the exam with Verilator, runs it, and (with
`--wave`) opens the resulting `.fst` waveform in Surfer. Pass
`--top <tb_module>` explicitly if the exam has more than one file in `tb/`.
Build output and waveforms land in `<exam>/sim/` (gitignored).

## Synthesis (Yosys)

```
uv run common/flow/opensource/synth/yosys/run_synth.py exams/2024-low-power-adder <top> --liberty /path/to/tech.lib
```

Reads all RTL under `<exam>/rtl/`, writes `<top>_netlist.v`/`.json` to
`<exam>/synth/`.

## Place & route (OpenROAD)

```
uv run common/flow/opensource/pnr/openroad/run_pnr.py exams/2024-low-power-adder <top>
```

Fill in `<exam>/pnr/config.tcl` first (LEF/LIB paths, utilization, placement
density). Runs the OpenROAD Docker image against the exam directory.
