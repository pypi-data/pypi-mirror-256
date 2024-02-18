"""The UI for Virtual Device class."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import os

from rapidstream.assets.device.device_factory import DeviceFactory
from rapidstream.assets.device.schedule import (
    ScheduleFactory,
    get_grid_one_iter_factory,
    get_grid_two_iter_factory,
)
from rapidstream.assets.device.virtual_device import VirtualDevice

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

U280_BOARD_NAME = "xilinx.com:au280:part0:1.1"
U280_PART_NAME = "xcu280-fsvh2892-2L-e"


def get_u280_default_device_factory() -> DeviceFactory:
    """Get a U280 default device factory."""
    df = DeviceFactory(
        num_row=3, num_col=2, part_num=U280_PART_NAME, board_name=U280_BOARD_NAME
    )

    # split into half SLR slots
    df.set_slot_area(0, 0, lut=220800, ff=441600, bram_18k=768, dsp=1440, uram=128)
    df.set_slot_area(1, 0, lut=218880, ff=437760, bram_18k=576, dsp=1440, uram=192)

    df.set_slot_area(0, 1, lut=220800, ff=441600, bram_18k=768, dsp=1536, uram=128)
    df.set_slot_area(1, 1, lut=218880, ff=437760, bram_18k=576, dsp=1536, uram=192)

    df.set_slot_area(0, 2, lut=220800, ff=441600, bram_18k=768, dsp=1536, uram=128)
    df.set_slot_area(1, 2, lut=218880, ff=437760, bram_18k=576, dsp=1536, uram=192)

    for x in range(2):
        for y in range(3):
            pblock = f"-add CLOCKREGION_X{x*4}Y{y*4}:CLOCKREGION_X{x*4+3}Y{y*4+3}"
            df.set_slot_pblock(x, y, [pblock])

    # set SLR crossing capacity
    for x in range(2):
        df.set_slot_capacity(x, 0, north=11520)
        df.set_slot_capacity(x, 1, north=11520)

        df.set_slot_capacity(x, 1, south=11520)
        df.set_slot_capacity(x, 2, south=11520)

    return df


def get_u280_default_device(output_path: str | None = None) -> VirtualDevice:
    """Get a U280 default device."""
    return get_u280_default_device_factory().generate_device(output_path)


def get_u280_vitis_device_factory(platform: str) -> DeviceFactory:
    """Get a U280 Vitis partition schedule."""
    df = get_u280_default_device_factory()

    if platform == "xilinx_u280_gen3x16_xdma_1_202211_1":
        df.set_slot_area(1, 0, lut=164160, ff=328320, bram_18k=432, dsp=1224, uram=192)
        df.set_slot_area(1, 1, lut=142080, ff=284160, bram_18k=384, dsp=1248, uram=192)
        df.set_slot_area(1, 2, lut=161760, ff=323520, bram_18k=432, dsp=1320, uram=192)

        df.set_slot_capacity(1, 0, north=8640)
        df.set_slot_capacity(1, 1, north=8640)

        df.set_slot_capacity(1, 1, south=8640)
        df.set_slot_capacity(1, 2, south=8640)

        return df

    raise ValueError(f"Unknown platform: {platform}")


def get_u280_default_schedule() -> ScheduleFactory:
    """Get a U280 default partition schedule."""
    return get_grid_one_iter_factory(3, 2)


def get_u280_two_level_factory() -> ScheduleFactory:
    """Get a U280 two-level partition schedule."""
    return get_grid_two_iter_factory(3, 2)
