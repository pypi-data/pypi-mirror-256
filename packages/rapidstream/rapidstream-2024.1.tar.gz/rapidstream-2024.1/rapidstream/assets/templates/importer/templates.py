"""Defining the driver to use importers."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import os
from glob import glob

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

HS_PP_MODULE = "__rs_hs_pipeline"
FF_PP_MODULE = "__rs_ff_pipeline"
AP_CTRL_PP_MODULE = "__rs_ap_ctrl_pipeline"
PASS_THROUGH_MODULE = "__rs_pass_through"

PP_MODULES = {
    HS_PP_MODULE,
    FF_PP_MODULE,
    AP_CTRL_PP_MODULE,
}

HANDSHAKE_ATOMIC_PP_UNITS = {
    "__rs_hs_pipeline_head",
    "__rs_hs_pipeline_tail",
    "__rs_hs_pipeline_body",
}

AP_CTRL_ATOMIC_PP_UNITS = {
    "__rs_ap_ctrl_pipeline_head_or_body",
    "__rs_ap_ctrl_pipeline_tail",
}

ATOMIC_PP_UNITS = {
    *HANDSHAKE_ATOMIC_PP_UNITS,
    *AP_CTRL_ATOMIC_PP_UNITS,
    "__rs_feed_forward_reg_group",
}

# check that all module names are in the RTL files
all_contents = ""  # pylint: disable=invalid-name
for rtl in glob(os.path.join(CURR_DIR, "*.v")):
    with open(rtl, "r", encoding="utf-8") as f:
        all_contents += f.read()
assert all(f"module {m}" in all_contents for m in PP_MODULES | ATOMIC_PP_UNITS)
