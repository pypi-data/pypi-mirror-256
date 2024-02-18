create_project -force cosim-project ./vivado -part xc7vx485tffg1157-1
set ORIG_RTL_PATH PLACEHOLDER
set rtl_files [glob -nocomplain ${ORIG_RTL_PATH}/*.v]
if {$rtl_files ne ""} {add_files -norecurse -scan_for_includes ${rtl_files} }
set rtl_files [glob -nocomplain ${ORIG_RTL_PATH}/*/*.v]
if {$rtl_files ne ""} {add_files -norecurse -scan_for_includes ${rtl_files} }
set rtl_files [glob -nocomplain ${ORIG_RTL_PATH}/*.sv]
if {$rtl_files ne ""} {add_files -norecurse -scan_for_includes ${rtl_files} }
set rtl_files [glob -nocomplain ${ORIG_RTL_PATH}/*/*.sv]
if {$rtl_files ne ""} {add_files -norecurse -scan_for_includes ${rtl_files} }
set tcl_files [glob -nocomplain ${ORIG_RTL_PATH}/*.tcl]
foreach ip_tcl ${tcl_files} { source ${ip_tcl} }
set tcl_files [glob -nocomplain ${ORIG_RTL_PATH}/*/*.tcl]
foreach ip_tcl ${tcl_files} { source ${ip_tcl} }
set xci_ip_files [glob -nocomplain ${ORIG_RTL_PATH}/*/*.xci]
if {$xci_ip_files ne ""} {add_files -norecurse -scan_for_includes ${xci_ip_files} }
set xci_ip_files [glob -nocomplain ${ORIG_RTL_PATH}/*.xci]
if {$xci_ip_files ne ""} {add_files -norecurse -scan_for_includes ${xci_ip_files} }
upgrade_ip -quiet [get_ips *]
set tb_files [glob PLACEHOLDER/*.v ]
set_property SOURCE_SET sources_1 [get_filesets sim_1]
add_files -fileset sim_1 -norecurse -scan_for_includes ${tb_files}
set_property top test [get_filesets sim_1]
set_property top_lib xil_defaultlib [get_filesets sim_1]
launch_simulation
run all
exit
