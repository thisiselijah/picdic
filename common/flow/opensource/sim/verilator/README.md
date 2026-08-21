# sim/verilator

Compiles and runs an exam's testbench with Verilator, dumps an FST waveform,
and optionally opens it in Surfer.

## Usage

```
uv run common/flow/opensource/sim/verilator/run_sim.py <exam_dir> [--top TB_TOP] [--wave]
```

- `<exam_dir>` — e.g. `exams/2024-low-power-adder`
- `--top` — testbench top module. Inferred automatically when `<exam_dir>/tb/`
  contains exactly one file; required if there's more than one.
- `--wave` — launch `surfer` on the resulting waveform after the run.

## Inputs

All `*.v`/`*.sv` under `<exam_dir>/rtl/` and `<exam_dir>/tb/`.

## Outputs

`<exam_dir>/sim/obj_dir/` (Verilator build) and `<exam_dir>/sim/*.fst`
(waveform dump). Both gitignored.

## Files

- `run_sim.py` — entry point; only file in this directory. There is no
  standalone Tcl/config file here since Verilator is invoked directly with
  CLI flags, unlike the synth/PnR flows.

## Prerequisites

Verilator and Surfer on `PATH` (`env/setup.sh` installs Surfer via Homebrew;
Verilator is expected to already be installed).
