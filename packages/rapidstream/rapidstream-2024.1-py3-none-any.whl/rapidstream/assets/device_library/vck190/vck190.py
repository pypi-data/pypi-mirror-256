"""The UI for Virtual Device class."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

from rapidstream.assets.device.device_factory import DeviceFactory
from rapidstream.assets.device.schedule import (
    ScheduleFactory,
    get_grid_one_iter_factory,
)
from rapidstream.assets.device.virtual_device import VirtualDevice

# 2023.2 only
VCK190_BOARD_NAME = "xilinx.com:vck190:part0:3.2"
VCK190_PART_NAME = "xcvc1902-vsva2197-2MP-e-S"


def get_vck190_default_device_factory() -> DeviceFactory:
    """Get a vck190 default device factory."""
    factory = DeviceFactory(
        num_row=2, num_col=2, part_num=VCK190_PART_NAME, board_name=VCK190_BOARD_NAME
    )

    # split into half SLR slots
    factory.set_slot_area(0, 0, lut=237952, ff=475904, bram_18k=504, dsp=564, uram=108)
    factory.set_slot_area(0, 1, lut=210560, ff=421120, bram_18k=426, dsp=420, uram=106)
    factory.set_slot_area(1, 0, lut=258688, ff=517376, bram_18k=576, dsp=564, uram=144)
    factory.set_slot_area(1, 1, lut=192640, ff=385280, bram_18k=428, dsp=420, uram=105)

    factory.set_slot_pblock(0, 0, ["-add CLOCKREGION_X0Y1:CLOCKREGION_X4Y2"])
    factory.set_slot_pblock(1, 0, ["-add CLOCKREGION_X5Y1:CLOCKREGION_X9Y2"])
    factory.set_slot_pblock(0, 1, ["-add CLOCKREGION_X0Y3:CLOCKREGION_X4Y4"])
    factory.set_slot_pblock(1, 1, ["-add CLOCKREGION_X5Y3:CLOCKREGION_X9Y4"])

    return factory


def get_vck190_default_device(output_path: str | None = None) -> VirtualDevice:
    """Get a vck190 default device."""
    return get_vck190_default_device_factory().generate_device(output_path)


def get_vck190_default_schedule() -> ScheduleFactory:
    """Get a vck190 default partition schedule."""
    return get_grid_one_iter_factory(2, 2)


if __name__ == "__main__":
    vck190 = get_vck190_default_device()
    with open("vck190.json", "w", encoding="utf-8") as f:
        f.write(vck190.model_dump_json(indent=2))
