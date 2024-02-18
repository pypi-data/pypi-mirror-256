# Copyright 2024 RapidStream Design Automation, Inc.
# All Rights Reserved.

######################################
# Auxiliary Procedures to print JSON
######################################

# Function to convert a list to a JSON array
proc listToJsonArray {lst} {
    set jsonArray "\["
    set first 1
    foreach item $lst {
        if {$first} {
            set first 0
        } else {
            append jsonArray ", "
        }
        append jsonArray "\"$item\""
    }
    append jsonArray "\]"
    return $jsonArray
}

# Function to convert a list of lists to JSON
proc listOfListsToJson {listOfLists} {
    set jsonOuterList "\["
    set first 1
    foreach innerList $listOfLists {
        if {$first} {
            set first 0
        } else {
            append jsonOuterList ", "
        }
        append jsonOuterList [listToJsonArray $innerList]
    }
    append jsonOuterList "\]"
    return $jsonOuterList
}

# Define the procedure to remove duplicates from a list
proc removeDuplicates {inputList} {
    # Create an empty associative array
    array set uniqueElements {}

    # Iterate over each element in the input list
    foreach element $inputList {
        # Add each element as a key in the associative array
        set uniqueElements($element) 1
    }

    # Return the unique elements (keys of the array)
    return [array names uniqueElements]
}


proc get_string { obj } {
    # add quotes around an object to be used in a json file
    return "\"${obj}\""
}

proc convert_dict_to_json { mydict filename } {
    # convert dict[str, list[str]] to a json file
    set lines {}
    foreach {key value} [dict get $mydict] {
        set key [get_string $key]
        set value [listToJsonArray $value]
        lappend lines "    ${key}: $value"
    }

    # sort the lines
    set lines [lsort $lines]

    set fp [open ${filename} w]
    if {[llength $lines] == 0} {
        # to match the style of rapidstream json format
        puts $fp "{}"
        close $fp
    } else {
        puts $fp "{"
        puts $fp [join $lines ",\n"]
        puts $fp "}"
        close $fp
    }
}

#################################
# Main Procedures
#################################

proc getBusName { inputString } {
    # get the bus name of a net
    # assume that nets will have xxx_yyy_zzz[\d+] format
    # and we will prune the [\d+] part if it exists
    set bracketIndex [string last "\[" $inputString]

    if {$bracketIndex != -1} {
        return [string range $inputString 0 [expr {$bracketIndex - 1}]]
    } else {
        return $inputString
    }
}

proc getCleanedBusNames { nets } {
    # note that bus nets will have the BUS_NAME property but scalar nets will not
    # so we create the USER_BUS_NAME property for scalar nets which is the same as
    # the net name

    # Concatenate BUS_NAME and USER_BUS_NAME properties of the nets
    set bus_names [concat [get_property BUS_NAME ${nets}] [get_property USER_BUS_NAME ${nets}]]

    # Remove duplicates by sorting and keeping only unique names
    set unique_bus_names [lsort -unique $bus_names]

    # Remove empty items from the list of unique bus names
    set no_empty_bus_names [lsearch -all -inline -not -exact $unique_bus_names ""]

    # Return the cleaned list of bus names
    return $no_empty_bus_names
}

proc getBusGroups { fileName } {
    # Get the related buses
    # the result must cover all buses in the module in order to analyze port connectivity

    # for each primitive cell, get the nets connected to the data pins (skip clk/rst/tied)
    # for each net, get the bus name
    set prim_cells [get_cells -hierarchical * -filter {IS_PRIMITIVE == 1}]

    set equiv_bus_groups {}
    foreach prim_cell ${prim_cells} {
        # should filter out const nets as well
        set data_pins [get_pins -quiet -of_objects ${prim_cell} -filter {IS_CLOCK == 0 && IS_RESET == 0 && IS_TIED == 0} ]
        set nets [get_nets -of_objects ${data_pins} -segments]

        if {[llength $nets] == 0} {
            continue
        }

        lappend equiv_bus_groups [getCleanedBusNames $nets]
    }

    # clk/rst nets and pass-through nets have not been added to the equiv_bus_groups
    # each of these nets should be a group by itself
    set clk_rst_nets [get_nets -of_objects [get_pins * -filter {IS_CLOCK == 1 || IS_RESET == 1}] -segments]
    set pass_through_wires [get_nets -filter {PIN_COUNT == 0}]
    set remaining_nets [concat $clk_rst_nets $pass_through_wires]
    set bus_names [getCleanedBusNames $remaining_nets]
    foreach bus_name ${bus_names} {
        lappend equiv_bus_groups [list $bus_name]
    }

    # remove duplicates
    set equiv_bus_groups [lsort -unique $equiv_bus_groups]

    set file [open ${fileName} "w"]
    puts $file [listOfListsToJson $equiv_bus_groups]
    close $file
}


proc getPortBusPairs { fileName } {
    # get a list of [bus_port, bus_net] pairs
    # note that it is much faster to get ports from nets than reversed

    # first get nets connected to ports in a batched command
    set port_nets [get_nets -of_objects [get_ports *] -filter {TYPE != "GROUND" && TYPE != "POWER"}]

    # for each net, get the connected port (seems fast) and add to port-net pairs
    set port_bus_pairs {}
    foreach port_net $port_nets {
        set ports [get_ports -of_objects $port_net]
        foreach port $ports {
            lappend port_bus_pairs [list [getBusName $port] [getBusName $port_net]]
        }
    }

    # remove duplicates
    set port_bus_pairs [lsort -unique $port_bus_pairs]

    set file [open ${fileName} "w"]
    puts $file [listOfListsToJson $port_bus_pairs]
    close $file
}


proc traceClkRstNetsToPorts { clk_rst_nets } {
    # helper function to trace clk/rst nets to original ports

    set clk_rst_portbits {}

    # Set to keep track of visited nets
    set visited_nets [dict create]

    # do a level-based traversal to get all clk/rst ports
    while {[llength $clk_rst_nets] > 0} {
        set clk_rst_portbits [concat ${clk_rst_portbits} [get_ports -of_objects $clk_rst_nets -filter {DIRECTION == "IN"}]]

        set upstream_pins [get_pins -quiet -of_objects $clk_rst_nets -filter {DIRECTION == "OUT"}]
        set upstream_cells [get_cells -quiet -of_objects $upstream_pins]

        # to get the next level of clk/rst nets, we do not consider clk/rst pins
        # not that we want to track the *data* propagation route from the initial clk/rst pins
        # for example, if we want to handle rst -> ff -> ff -> broadcast to all cells
        # we need to track the data propagation route from the initial rst pin
        set next_iter_pins [get_pins -quiet -of_objects $upstream_cells -filter {DIRECTION == "IN" && IS_CLOCK == 0 && IS_RESET == 0}]
        set next_clk_rst_nets [get_nets -quiet -segments -of_objects $next_iter_pins]

        # Update clk_rst_nets with nets that have not been visited
        set new_nets {}
        foreach net $next_clk_rst_nets {
            if { [dict exists $visited_nets $net] } {
                continue
            }
            lappend new_nets $net
            dict set visited_nets $net 1
        }
        set clk_rst_nets $new_nets
    }

    return [removeDuplicates $clk_rst_portbits]
}


proc getClkRstInputs { clkFileName rstFileName } {
    # get the top-level clk/rst input ports

    set clk_nets [get_nets -segments -of_objects [get_pins * -filter {IS_CLOCK == 1}]]
    set clk_portbits [traceClkRstNetsToPorts $clk_nets]

    set file [open ${clkFileName} "w"]
    puts $file [listToJsonArray $clk_portbits]
    close $file

    set rst_nets [get_nets -segments -of_objects [get_pins * -filter {IS_RESET == 1}]]
    set rst_portbits [traceClkRstNetsToPorts $rst_nets]

    set file [open ${rstFileName} "w"]
    puts $file [listToJsonArray $rst_portbits]
    close $file
}


proc getEquivalenPortPairs { fileName } {
    # Get pairs of bus ports that are connected by wire
    # the output pair has the format [input_portbit, output_portbit]

    # get all nets that are not connected to any pins of internal logic element
    set pass_through_nets [get_nets -filter {PIN_COUNT == 0 && TYPE != "POWER" && TYPE != "GROUND"}]

    set passthrough_portbit_pairs {}
    foreach net ${pass_through_nets} {
        set input_portbit [get_ports -of_objects $net -filter {DIRECTION == "IN"}]
        set output_portbits [get_ports -of_objects $net -filter {DIRECTION == "OUT"}]

        # check that there is at most one input port
        if {[llength $input_portbit] > 1} {
            error "More than one input port for net ${net}"
        }

        # if no input port, skip
        if {[llength $input_portbit] == 0} {
            continue
        }

        foreach portbit $output_portbits {
            lappend passthrough_portbit_pairs [list $input_portbit $portbit]
        }
    }

    set file [open ${fileName} "w"]
    puts $file [listOfListsToJson $passthrough_portbit_pairs]
    close $file
}

proc getPortbitList { fileName } {
    # get a list of individual ports

    set file [open ${fileName} "w"]
    puts $file [listToJsonArray [get_ports *]]
    close $file
}


proc getUnconnectedPortbits { fileName } {
    # get a list of unconnected ports.
    # we only treat a port as unconnected if all portbits are unconnected

    set unconnected_portbits [get_ports -filter {UNCONNECTED == "true"}]

    set file [open ${fileName} "w"]
    puts $file [listToJsonArray ${unconnected_portbits}]
    close $file
}


proc getVccPortbits { fileName } {
    # get a list of vcc portbits

    set vcc_portbits [get_ports -of_objects [get_nets -filter {TYPE == "POWER"}]]

    set file [open ${fileName} "w"]
    puts $file [listToJsonArray [removeDuplicates $vcc_portbits]]
    close $file

}


proc getGndPortbits { fileName } {
    # get a list of vcc portbits

    set gnd_portbits [get_ports -of_objects [get_nets -filter {TYPE == "GROUND"}]]

    set file [open ${fileName} "w"]
    puts $file [listToJsonArray [removeDuplicates $gnd_portbits]]
    close $file

}


proc getArea { fileName } {
    # get the area of the design
    # only create a tag file "tiny_aux" if the area is very small

    set TAG_NAME "tiny_aux"

    # case 1: if the post-elaboration cell-count is alreay very small, no need to synth
    # in this case, no utilization report will be created
    set cell_count [llength [get_cells -hierarchical *]]
    if {$cell_count < 2000} {
        puts "Post-elab cell count is ${cell_count}, skip synthesis"
        set file [open ${TAG_NAME} "w"]
        close $file
        return
    }

    # case 2: if the post-elaboration cell-count is large, run synthesis to get area
    puts "Post-elab cell count is ${cell_count}, run synthesis to get accurate area"
    synth_design -mode out_of_context -no_timing_driven -directive RuntimeOptimized
    report_utilization -file ${fileName} -hierarchical
}

# create USER_BUS_NAME property for non-bus nets
create_property USER_BUS_NAME net
foreach net [get_nets -filter {BUS_NAME == ""}] {
    set_property USER_BUS_NAME $net $net
}

getBusGroups "equiv_bus_groups.json"
getClkRstInputs "clk_input_portbits.json" "rst_input_portbits.json"
getPortBusPairs "port_to_bus.json"
getEquivalenPortPairs "wired_input_output_portbit_pairs.json"
getPortbitList "portbit_list.json"
getUnconnectedPortbits "unconnected_portbits.json"
getVccPortbits "vcc_portbits.json"
getGndPortbits "gnd_portbits.json"
getArea "utilization.rpt"
