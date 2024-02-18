"""The UI for Virtual Device class."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

from rapidstream.assets.device.virtual_device import (
    WIRE_CAPACITY_INF,
    Area,
    VirtualDevice,
    VirtualSlot,
)


class DeviceFactory:  # pylint: disable=too-many-instance-attributes
    """User interface to create a virtual device."""

    def __init__(
        self, num_row: int, num_col: int, part_num: str, board_name: str | None
    ) -> None:
        """Init."""
        self.num_row = num_row
        self.num_col = num_col
        self.part_num = part_num
        self.board_name = board_name

        self.unit_dist_x = 100
        self.unit_dist_y = 150  # penalty for vertical routing through SLR boundary
        self.pp_dist: int = 100

        empty_area = Area(lut=0, ff=0, bram_18k=0, dsp=0, uram=0)
        self.coor_to_area: dict[int, dict[int, Area]] = {
            i: {j: empty_area for j in range(num_row)} for i in range(num_col)
        }
        self.coor_to_pblock: dict[int, dict[int, list[str] | None]] = {
            i: {j: None for j in range(num_row)} for i in range(num_col)
        }
        self.coor_to_capacity = [
            [
                {
                    "NORTH": WIRE_CAPACITY_INF,
                    "SOUTH": WIRE_CAPACITY_INF,
                    "EAST": WIRE_CAPACITY_INF,
                    "WEST": WIRE_CAPACITY_INF,
                }
                for _ in range(num_row)
            ]
            for _ in range(num_col)
        ]

    def set_slot_area(
        self,
        x: int,
        y: int,
        lut: int = 0,
        ff: int = 0,
        bram_18k: int = 0,
        dsp: int = 0,
        uram: int = 0,
    ) -> None:
        """Set the area of a slot."""
        assert 0 <= x < self.num_col
        assert 0 <= y < self.num_row
        self.coor_to_area[x][y] = Area(
            lut=lut, ff=ff, bram_18k=bram_18k, dsp=dsp, uram=uram
        )

    def reduce_slot_area(
        self,
        x: int,
        y: int,
        lut: int = 0,
        ff: int = 0,
        bram_18k: int = 0,
        dsp: int = 0,
        uram: int = 0,
    ) -> None:
        """Reduce the available area of a given slot."""
        assert 0 <= x < self.num_col
        assert 0 <= y < self.num_row
        self.coor_to_area[x][y] = Area(
            lut=self.coor_to_area[x][y].lut - lut,
            ff=self.coor_to_area[x][y].ff - ff,
            bram_18k=self.coor_to_area[x][y].bram_18k - bram_18k,
            dsp=self.coor_to_area[x][y].dsp - dsp,
            uram=self.coor_to_area[x][y].uram - uram,
        )

    def set_slot_capacity(
        self,
        x: int,
        y: int,
        north: int = WIRE_CAPACITY_INF,
        south: int = WIRE_CAPACITY_INF,
        east: int = WIRE_CAPACITY_INF,
        west: int = WIRE_CAPACITY_INF,
    ) -> None:
        """Set the wire capacity of a slot."""
        self.coor_to_capacity[x][y] = {
            "NORTH": north,
            "SOUTH": south,
            "EAST": east,
            "WEST": west,
        }

    def set_slot_pblock(self, x: int, y: int, pblock_ranges: list[str]) -> None:
        """Set the pblock of a slot."""
        for line in pblock_ranges:
            if not line.startswith(("-add", "-remove")):
                raise ValueError(
                    f"Pblock range must starts with -add or -remove: {line}"
                )

        self.coor_to_pblock[x][y] = pblock_ranges

    def generate_device(self, output_path: str | None = None) -> VirtualDevice:
        """Generate a virtual device."""
        slots = []
        for x in range(self.num_col):
            slot_row = []
            for y in range(self.num_row):
                slot_row.append(
                    VirtualSlot(
                        area=self.coor_to_area[x][y],
                        centroid_x_coor=self.unit_dist_x * x,
                        centroid_y_coor=self.unit_dist_y * y,
                        pblock_ranges=self.coor_to_pblock[x][y],
                        north_wire_capacity=self.coor_to_capacity[x][y]["NORTH"],
                        south_wire_capacity=self.coor_to_capacity[x][y]["SOUTH"],
                        east_wire_capacity=self.coor_to_capacity[x][y]["EAST"],
                        west_wire_capacity=self.coor_to_capacity[x][y]["WEST"],
                    )
                )
            slots.append(slot_row)

        device = VirtualDevice(
            slots=slots,
            num_rows=self.num_row,
            num_cols=self.num_col,
            pp_dist=self.pp_dist,
            part_num=self.part_num,
            board_name=self.board_name,
        )

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(device.model_dump_json(indent=2))

        return device
