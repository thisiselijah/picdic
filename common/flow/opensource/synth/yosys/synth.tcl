# Generic Yosys gate-level synthesis script.
# Invoked by common/flow/opensource/synth/yosys/run_synth.py - not meant to be
# called directly.
# Usage: yosys -c common/flow/opensource/synth/yosys/synth.tcl \
#          -- <top_module> <rtl_dir> <liberty_lib> <out_dir>

set top     [lindex $argv 0]
set rtl_dir [lindex $argv 1]
set liberty [lindex $argv 2]
set out_dir [lindex $argv 3]

foreach pattern {*.v *.sv} {
    foreach f [glob -nocomplain $rtl_dir/$pattern] {
        read_verilog -sv $f
    }
}

hierarchy -check -top $top
proc; opt; fsm; opt; memory; opt
techmap; opt

dfflibmap -liberty $liberty
abc -liberty $liberty
opt_clean -purge

stat -liberty $liberty
check

write_verilog -noattr $out_dir/${top}_netlist.v
write_json $out_dir/${top}_netlist.json
