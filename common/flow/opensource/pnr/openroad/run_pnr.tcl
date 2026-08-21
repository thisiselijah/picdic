# Generic OpenROAD place-and-route script (floorplan -> place -> CTS -> route -> GDS).
# Invoked by run_pnr.sh inside the OpenROAD docker container.
# Expects -top <module> and reads netlist/constraints/lib/lef paths from pnr/config.mk-style vars.

source pnr/config.tcl

read_lef $LEF_FILES
read_liberty $LIB_FILES
read_verilog synth/${TOP}_netlist.v
link_design $TOP
read_sdc constraints/${TOP}.sdc

initialize_floorplan -utilization $FP_UTIL -aspect_ratio 1.0 -core_space 2.0
place_pins -random

global_placement -density $PLACE_DENSITY
detailed_placement

clock_tree_synthesis -root_buf $CTS_BUF -buf_list $CTS_BUF

global_route
detailed_route

write_def pnr/${TOP}_final.def
write_verilog pnr/${TOP}_final.v
write_gds pnr/${TOP}_final.gds

report_checks
report_wns
report_tns
report_design_area
