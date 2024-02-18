"""Record the pre-defined board library."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

from rapidstream.assets.device.schedule import ScheduleFactory
from rapidstream.assets.device.virtual_device import VirtualDevice
from rapidstream.assets.device_library.u50.u50 import (
    U50_BOARD_NAME,
    U50_PART_NAME,
    get_u50_default_device,
    get_u50_default_schedule,
)
from rapidstream.assets.device_library.u250.u250 import (
    U250_BOARD_NAME,
    U250_PART_NAME,
    get_u250_default_device,
    get_u250_two_level_schedule,
)
from rapidstream.assets.device_library.u280.u280 import (
    U280_BOARD_NAME,
    U280_PART_NAME,
    get_u280_default_device,
    get_u280_default_schedule,
)
from rapidstream.assets.device_library.vck190.vck190 import (
    VCK190_BOARD_NAME,
    VCK190_PART_NAME,
    get_vck190_default_device,
    get_vck190_default_schedule,
)

U50_NAMES = {"U50", "u50", U50_BOARD_NAME, U50_PART_NAME}
U280_NAMES = {"U280", "u280", U280_BOARD_NAME, U280_PART_NAME}
U250_NAMES = {"U250", "u250", U250_BOARD_NAME, U250_PART_NAME}
VCK190_NAMES = {"VCK190", "vck190", VCK190_BOARD_NAME, VCK190_PART_NAME}

__all__ = [
    "U250_BOARD_NAME",
    "U250_PART_NAME",
    "U280_BOARD_NAME",
    "U280_PART_NAME",
    "U50_BOARD_NAME",
    "U50_PART_NAME",
    "VCK190_BOARD_NAME",
    "VCK190_PART_NAME",
    "get_default_device",
    "get_default_partition_schedule",
]


def get_default_device(board_name: str) -> VirtualDevice:
    """Get the default device for a board."""
    if board_name in U50_NAMES:
        return get_u50_default_device()
    elif board_name in U280_NAMES:
        return get_u280_default_device()
    elif board_name in U250_NAMES:
        return get_u250_default_device()
    elif board_name in VCK190_NAMES:
        return get_vck190_default_device()
    else:
        raise ValueError(f"Unsupported board name: {board_name}")


def get_default_partition_schedule(board_name: str) -> ScheduleFactory:
    """Get the default partition schedule for a board."""
    if board_name in U50_NAMES:
        return get_u50_default_schedule()
    elif board_name in U280_NAMES:
        return get_u280_default_schedule()
    elif board_name in U250_NAMES:
        return get_u250_two_level_schedule()
    elif board_name in VCK190_NAMES:
        return get_vck190_default_schedule()
    else:
        raise ValueError(f"Unsupported board name: {board_name}")
