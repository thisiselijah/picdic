# pnr/openroad

Place-and-route for an exam via the OpenROAD Docker image (ORFS),
floorplan → placement → CTS → routing → GDS.

## Usage

```
uv run common/flow/opensource/pnr/openroad/run_pnr.py <exam_dir> <top>
```

- `<exam_dir>` — e.g. `exams/2024-low-power-adder`
- `<top>` — top module name

Before running, fill in `<exam_dir>/pnr/config.tcl` (copied from
`exams/_template/pnr/config.tcl`): `LEF_FILES`, `LIB_FILES`, `FP_UTIL`,
`PLACE_DENSITY`, `CTS_BUF`.

## Inputs

- `<exam_dir>/synth/<top>_netlist.v` (from the yosys synth flow)
- `<exam_dir>/constraints/<top>.sdc`
- `<exam_dir>/pnr/config.tcl`

## Outputs

`<exam_dir>/pnr/<top>_final.def`, `.v`, `.gds`, plus timing/area reports
printed to the container log.

## Files

- `run_pnr.py` — entry point; mounts `<exam_dir>` into the `openroad/orfs`
  container at `/workspace` and runs OpenROAD against `run_pnr.tcl`.
- `run_pnr.tcl` — the actual OpenROAD script, run inside the container.
  Sources the per-exam `pnr/config.tcl` for library/floorplan parameters. Not
  meant to be invoked directly — always go through `run_pnr.py`.

## Prerequisites

Docker, with the image pulled once:

```
docker pull openroad/orfs:latest
```
