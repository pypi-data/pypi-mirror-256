"""Public assets of RapidStream."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

DATAFLOW_DIR = os.path.join(CURR_DIR, "dataflow")
RUN_COSIM_TCL = os.path.join(CURR_DIR, "tcls", "run_cosim.tcl")
GET_NETLIST_INFO_TCL = os.path.join(CURR_DIR, "tcls", "get_netlist_info.tcl")
PACKAGE_XO_TCL = os.path.join(CURR_DIR, "tcls", "package_xo.tcl")
EXPORTER_TEMPLATES_DIR = os.path.join(CURR_DIR, "templates", "exporter")
IMPORTER_TEMPLATES_DIR = os.path.join(CURR_DIR, "templates", "importer")
VPP_TEMPLATE = os.path.join(CURR_DIR, "templates", "vpp", "vpp_template.sh")

__ALL__ = [
    "RUN_COSIM_TCL",
    "DATAFLOW_DIR",
    "EXPORTER_TEMPLATES_DIR",
    "IMPORTER_TEMPLATES_DIR",
    "GET_NETLIST_INFO_TCL",
    "PACKAGE_XO_TCL",
    "DUMMY_DCP_PATH",
    "VPP_TEMPLATE",
]
