# synth/yosys

Gate-level synthesis of an exam's RTL with Yosys.

## Usage

```
uv run common/flow/opensource/synth/yosys/run_synth.py <exam_dir> <top> --liberty <path>
```

- `<exam_dir>` — e.g. `exams/2024-low-power-adder`
- `<top>` — top module name
- `--liberty` — path to the tech `.lib` file (from a PDK; not committed to
  this repo, see `.gitignore`)

## Inputs

All `*.v`/`*.sv` under `<exam_dir>/rtl/`.

## Outputs

`<exam_dir>/synth/<top>_netlist.v` and `<exam_dir>/synth/<top>_netlist.json`.

## Files

- `run_synth.py` — entry point; builds the `yosys -c synth.tcl -- ...`
  invocation and validates paths before running.
- `synth.tcl` — the actual Yosys script (hierarchy check, generic opt, techmap,
  `dfflibmap`/`abc` against the liberty lib, netlist writeback). Not meant to
  be invoked directly — always go through `run_synth.py`.

## Prerequisites

`yosys` on `PATH` (`env/setup.sh` installs it via Homebrew).
