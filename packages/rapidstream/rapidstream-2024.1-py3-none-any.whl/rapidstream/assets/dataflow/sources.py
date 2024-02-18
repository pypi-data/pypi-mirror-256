"""List of RTL IP files for dataflow designs."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""


import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

ISLAND_SYNTH_IP_FILES = [
    f"{CURR_DIR}/ip/stream_fmacc_synth.v",
    f"{CURR_DIR}/ip/lutram.v",
]

assert all(os.path.isfile(path) for path in ISLAND_SYNTH_IP_FILES)
