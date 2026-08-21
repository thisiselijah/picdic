# Synopsys Design Compiler (dc_shell) gate-level synthesis template.
# Usage: dc_shell -f common/flow/commercial/synth/dc/run_dc.tcl \
#          -x "set TOP <top>; set RTL_GLOB <glob>; set OUT_DIR <exam>/synth"
#
# Requires site-specific target/link libraries set via $TARGET_LIBS / $LINK_LIBS
# (e.g. in ~/.synopsys_dc.setup or exported before invoking dc_shell).

set_app_var target_library $env(TARGET_LIBS)
set_app_var link_library   "* $env(TARGET_LIBS)"

analyze -format sverilog [glob $RTL_GLOB]
elaborate $TOP
current_design $TOP
link
check_design

read_sdc $CONSTRAINTS_FILE

compile_ultra

write -format verilog -hierarchy -output $OUT_DIR/${TOP}_netlist.v
write_sdc $OUT_DIR/${TOP}.sdc
report_timing > $OUT_DIR/${TOP}_timing.rpt
report_area   > $OUT_DIR/${TOP}_area.rpt
report_power  > $OUT_DIR/${TOP}_power.rpt

exit
