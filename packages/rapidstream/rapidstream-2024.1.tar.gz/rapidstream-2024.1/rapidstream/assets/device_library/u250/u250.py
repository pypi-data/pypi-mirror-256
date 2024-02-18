"""The UI for Virtual Device class."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import os

from rapidstream.assets.device.device_factory import DeviceFactory
from rapidstream.assets.device.schedule import (
    ScheduleFactory,
    get_grid_two_iter_factory,
)
from rapidstream.assets.device.virtual_device import VirtualDevice

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

U250_BOARD_NAME = "xilinx.com:au250:part0:1.3"
U250_PART_NAME = "xcu250-figd2104-2L-e"


def get_u250_default_device_factory() -> DeviceFactory:
    """Get a U250 default device factory."""
    df = DeviceFactory(
        num_row=4, num_col=2, part_num=U250_PART_NAME, board_name=U250_BOARD_NAME
    )

    # split into half SLR slots
    for y in range(4):
        df.set_slot_area(0, y, lut=216960, ff=433920, bram_18k=768, dsp=1536, uram=128)
        df.set_slot_area(1, y, lut=215040, ff=430080, bram_18k=576, dsp=1536, uram=192)

    for x in range(2):
        for y in range(4):
            pblock = f"-add CLOCKREGION_X{x*4}Y{y*4}:CLOCKREGION_X{x*4+3}Y{y*4+3}"
            df.set_slot_pblock(x, y, [pblock])

    # set SLR crossing capacity
    for x in range(2):
        df.set_slot_capacity(x, 0, north=11520)
        df.set_slot_capacity(x, 1, north=11520)
        df.set_slot_capacity(x, 2, north=11520)

        df.set_slot_capacity(x, 1, south=11520)
        df.set_slot_capacity(x, 2, south=11520)
        df.set_slot_capacity(x, 3, south=11520)

    return df


def get_u250_default_device(output_path: str | None = None) -> VirtualDevice:
    """Get a U250 default device."""
    return get_u250_default_device_factory().generate_device(output_path)


def get_u250_two_level_schedule() -> ScheduleFactory:
    """Get a U250 two-level partition schedule."""
    return get_grid_two_iter_factory(4, 2)
