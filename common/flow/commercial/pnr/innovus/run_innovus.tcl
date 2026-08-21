# Cadence Innovus place-and-route template.
# Usage: innovus -files common/flow/commercial/pnr/innovus/run_innovus.tcl \
#          -log pnr.log
#
# Requires TOP / LEF_FILES / LIB_FILES / NETLIST / SDC_FILE / OUT_DIR to be
# exported as env vars or set before sourcing this file.

set init_lef_file       $env(LEF_FILES)
set init_verilog        $env(NETLIST)
set init_top_cell       $env(TOP)
set init_mmmc_file      $env(MMMC_FILE)

init_design

floorPlan -site core -r 1.0 0.7 2.0 2.0 2.0 2.0

place_opt_design

ccopt_design

routeDesign

setExtractRCMode -engine postRoute
extractRC
report_timing > $env(OUT_DIR)/$env(TOP)_timing.rpt

streamOut $env(OUT_DIR)/$env(TOP)_final.gds \
  -mapFile $env(GDS_MAP_FILE) -libName DESIGN -structureName $env(TOP)

saveDesign $env(OUT_DIR)/$env(TOP)_final.enc
exit
