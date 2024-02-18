"""The Virtual Device class."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import logging
import math
import re
from typing import Any

from pydantic import BaseModel, ConfigDict

from rapidstream.assets.device.common import Coor

WIRE_CAPACITY_INF = 10**8
_logger = logging.getLogger(__name__)


class Area(BaseModel):
    """Represents an area."""

    model_config = ConfigDict(frozen=True)

    lut: int
    ff: int
    bram_18k: int
    dsp: int
    uram: int

    def __init__(self, **data: Any) -> None:
        """Init and check all values are non-negative."""
        super().__init__(**data)

        if not all(value >= 0 for value in self.to_dict().values()):
            raise ValueError(f"All area values must be non-negative: {self.to_dict()}")

    def to_dict(self) -> dict[str, int]:
        """For compatibility with old code."""
        return {
            "LUT": self.lut,
            "FF": self.ff,
            "BRAM_18K": self.bram_18k,
            "DSP": self.dsp,
            "URAM": self.uram,
        }


def sum_area(areas: list[Area]) -> Area:
    """Sum up a list of areas."""
    return Area(
        lut=sum(area.lut for area in areas),
        ff=sum(area.ff for area in areas),
        bram_18k=sum(area.bram_18k for area in areas),
        dsp=sum(area.dsp for area in areas),
        uram=sum(area.uram for area in areas),
    )


class VirtualSlot(BaseModel):
    """Represents a virtual slot."""

    model_config = ConfigDict(frozen=True)

    area: Area
    centroid_x_coor: int
    centroid_y_coor: int
    pblock_ranges: list[str] | None = None
    north_wire_capacity: int = WIRE_CAPACITY_INF
    south_wire_capacity: int = WIRE_CAPACITY_INF
    east_wire_capacity: int = WIRE_CAPACITY_INF
    west_wire_capacity: int = WIRE_CAPACITY_INF

    def __init__(self, **data: Any) -> None:
        """Init with extra validation."""
        super().__init__(**data)

        if self.pblock_ranges is not None:
            assert all(
                re.match(r"(-add|-remove)[ ]+\w+_X\d+Y\d+:\w+_X\d+Y\d+", pblock_range)
                for pblock_range in self.pblock_ranges
            )


class VirtualDevice(BaseModel):
    """Represents a virtual device."""

    slots: list[list[VirtualSlot]]
    num_rows: int
    num_cols: int
    pp_dist: int
    part_num: str
    board_name: str | None

    model_config = ConfigDict(frozen=True)

    def __init__(self, **data: Any) -> None:
        """Init with extra validation."""
        super().__init__(**data)

        assert len(self.slots) == self.num_cols
        assert all(len(row) == self.num_rows for row in self.slots)

    def get_num_col(self) -> int:
        """Get the number of columns."""
        return self.num_cols

    def get_num_row(self) -> int:
        """Get the number of rows."""
        return self.num_rows

    def get_slot(self, x: int, y: int) -> VirtualSlot:
        """Get a slot."""
        return self.slots[x][y]

    def get_island_centroid(self, coor: Coor) -> dict[str, float]:
        """Get the centroid of an island."""
        dl_slot = self.get_slot(coor.down_left_x, coor.down_left_y)
        ur_slot = self.get_slot(coor.up_right_x, coor.up_right_y)

        island_centroid_x = (dl_slot.centroid_x_coor + ur_slot.centroid_x_coor) / 2
        island_centroid_y = (dl_slot.centroid_y_coor + ur_slot.centroid_y_coor) / 2

        return {"x": island_centroid_x, "y": island_centroid_y}

    def get_island_area(self, coor: Coor) -> Area:
        """Get the area of an island."""
        areas = [self.get_slot(x, y).area for x, y in coor.get_all_slot_coors()]
        return sum_area(areas)

    def get_slot_north_wire_capacity(self, x: int, y: int) -> int:
        """Get the north wire capacity of a slot."""
        return self.get_slot(x, y).north_wire_capacity

    def get_slot_south_wire_capacity(self, x: int, y: int) -> int:
        """Get the south wire capacity of a slot."""
        return self.get_slot(x, y).south_wire_capacity

    def get_slot_east_wire_capacity(self, x: int, y: int) -> int:
        """Get the east wire capacity of a slot."""
        return self.get_slot(x, y).east_wire_capacity

    def get_slot_west_wire_capacity(self, x: int, y: int) -> int:
        """Get the west wire capacity of a slot."""
        return self.get_slot(x, y).west_wire_capacity

    def get_island_pblock_range(self, coor: Coor) -> str:
        """Get the pblock range of an island."""
        island_ranges = []
        for x, y in coor.get_all_slot_coors():
            slot_ranges = self.get_slot(x, y).pblock_ranges
            if slot_ranges is None:
                raise ValueError(f"Slot (%d, %d) does not have a pblock range", x, y)

            island_ranges += slot_ranges

        assert all(line.startswith(("-add", "-remove")) for line in island_ranges)

        # FIXME: do not join
        # FIXME: here we must use space to join because we later need to split them.
        return " ".join(island_ranges)

    def get_pipeline_level(self, src_island: Coor, sink_island: Coor) -> int:
        """Get the pipeline level between two slots."""
        src_centroid = self.get_island_centroid(src_island)
        sink_centroid = self.get_island_centroid(sink_island)

        dist_x = abs(src_centroid["x"] - sink_centroid["x"])
        dist_y = abs(src_centroid["y"] - sink_centroid["y"])

        pp_x = dist_x / self.pp_dist
        pp_y = dist_y / self.pp_dist

        # if the source and sink have the same x coordinate, no pipeline is needed
        # otherwise at least one pipeline stage is needed for x direction

        if dist_x != 0:
            pp_x = max(pp_x, 1)

        if dist_y != 0:
            pp_y = max(pp_y, 1)

        return math.ceil(pp_x + pp_y)
