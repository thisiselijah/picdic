#!/usr/bin/env bash
# Installs/checks the open-source gate-level + physical design toolchain on macOS.
# Commercial tools (Synopsys/Cadence) are not installable here - they require
# your own licensed install; see common/flow/commercial/ for script templates
# and set TARGET_LIBS / MMMC_FILE / etc. per your site setup.
set -euo pipefail

echo "== Homebrew formulae =="
# verilator is already installed and used for simulation; not reinstalled here.
brew install yosys magic ngspice surfer uv || true

echo "== Python dev environment (uv) =="
uv sync || true

echo "== KLayout (GDS viewer/DRC) =="
brew install --cask klayout || true

echo "== OpenROAD (via Docker, RTL-to-GDSII P&R) =="
if command -v docker >/dev/null; then
  echo "Pulling openroad/orfs:latest (several GB, run manually if you'd rather defer):"
  echo "  docker pull openroad/orfs:latest"
else
  echo "Docker not found - install Docker Desktop first: https://www.docker.com/products/docker-desktop"
fi

echo "== Verification =="
for t in yosys verilator magic ngspice surfer uv; do
  command -v $t >/dev/null && echo "OK   $t: $(command -v $t)" || echo "MISS $t"
done
command -v klayout >/dev/null && echo "OK   klayout" || echo "MISS klayout (may need: open /Applications/klayout.app once to finish setup)"
