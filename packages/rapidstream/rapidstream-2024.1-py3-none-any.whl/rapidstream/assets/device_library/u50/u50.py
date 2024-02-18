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

U50_BOARD_NAME = "xilinx.com:au50dd:part0:1.0"
U50_PART_NAME = "xcu50-fsvh2104-2-e"


def get_u50_default_device_factory() -> DeviceFactory:
    """Get a U50 default device factory."""
    factory = DeviceFactory(
        num_row=2,
        num_col=2,
        part_num=U50_PART_NAME,
        board_name=U50_BOARD_NAME,
    )

    # split into half SLR slots
    factory.set_slot_area(0, 0, lut=220800, ff=441600, bram_18k=768, dsp=1440, uram=128)
    factory.set_slot_area(1, 0, lut=218880, ff=437760, bram_18k=576, dsp=1440, uram=192)
    factory.set_slot_area(0, 1, lut=216960, ff=433920, bram_18k=768, dsp=1536, uram=128)
    factory.set_slot_area(1, 1, lut=215040, ff=430080, bram_18k=576, dsp=1536, uram=192)

    factory.set_slot_pblock(0, 0, ["-add CLOCKREGION_X0Y0:CLOCKREGION_X3Y3"])
    factory.set_slot_pblock(1, 0, ["-add CLOCKREGION_X4Y0:CLOCKREGION_X7Y3"])
    factory.set_slot_pblock(0, 1, ["-add CLOCKREGION_X0Y4:CLOCKREGION_X3Y7"])
    factory.set_slot_pblock(1, 1, ["-add CLOCKREGION_X4Y4:CLOCKREGION_X7Y7"])

    # set SLR crossing capacity
    factory.set_slot_capacity(0, 0, north=11520)
    factory.set_slot_capacity(0, 1, south=11520)
    factory.set_slot_capacity(1, 0, north=11520)
    factory.set_slot_capacity(1, 1, south=11520)

    return factory


def get_u50_default_device(output_path: str | None = None) -> VirtualDevice:
    """Get a U50 default device."""
    factory = get_u50_default_device_factory()
    return factory.generate_device(output_path)


def get_u50_vitis_device_factory(platform: str) -> DeviceFactory:
    """Get a U50 Vitis device."""
    factory = get_u50_default_device_factory()

    if platform == "xilinx_u50_gen3x16_xdma_5_202210_1":
        # shell region on the right side of SLR 0
        factory.reduce_slot_area(
            1, 0, lut=87840, ff=175680, bram_18k=240, dsp=528, uram=48
        )

        # shell region on the right side of SLR 1
        factory.reduce_slot_area(
            1, 1, lut=78320, ff=156640, bram_18k=216, dsp=504, uram=48
        )

        # vitis region takes away half of the Lagunas
        factory.set_slot_capacity(1, 0, north=int(11520 / 2))
        factory.set_slot_capacity(1, 1, south=int(11520 / 2))

        slot_x1y0_ranges = [
            "-add CLOCKREGION_X4Y2:CLOCKREGION_X5Y3",
            "-add CLOCKREGION_X5Y1:CLOCKREGION_X5Y1",
            "-add CLOCKREGION_X4Y0:CLOCKREGION_X6Y0",
            "-add URAM288_X2Y16:URAM288_X2Y31",
            "-add RAMB36_X8Y12:RAMB36_X9Y23",
            "-add RAMB36_X12Y0:RAMB36_X13Y5",
            "-add RAMB18_X8Y24:RAMB18_X9Y47",
            "-add RAMB18_X12Y0:RAMB18_X13Y11",
            "-add DSP48E2_X16Y18:DSP48E2_X19Y41",
            "-add DSP48E2_X30Y0:DSP48E2_X31Y5",
            "-add BLI_HBM_AXI_INTF_X30Y0:BLI_HBM_AXI_INTF_X31Y0",
            "-add BLI_HBM_APB_INTF_X30Y0:BLI_HBM_APB_INTF_X31Y0",
            "-add SLICE_X117Y60:SLICE_X145Y119",
            "-add SLICE_X206Y0:SLICE_X232Y29",
        ]

        slot_x1y1_ranges = [
            "-add CLOCKREGION_X4Y7:CLOCKREGION_X7Y7",
            "-add CLOCKREGION_X4Y5:CLOCKREGION_X5Y6",
            "-add CLOCKREGION_X5Y4:CLOCKREGION_X5Y4",
            "-add URAM288_X2Y64:URAM288_X2Y79",
            "-add RAMB36_X8Y48:RAMB36_X9Y59",
            "-add RAMB18_X8Y96:RAMB18_X9Y119",
            "-add LAGUNA_X16Y120:LAGUNA_X19Y239",
            "-add DSP48E2_X16Y90:DSP48E2_X19Y113",
            "-add CONFIG_SITE_X0Y1:CONFIG_SITE_X0Y1",
            "-add SLICE_X220Y331:SLICE_X221Y359",
            "-add SLICE_X176Y325:SLICE_X221Y330",
            "-add SLICE_X220Y300:SLICE_X221Y324",
            "-add SLICE_X140Y240:SLICE_X145Y299",
            "-add SLICE_X125Y240:SLICE_X138Y299",
            "-add SLICE_X117Y240:SLICE_X123Y299",
        ]
        factory.set_slot_pblock(1, 0, slot_x1y0_ranges)
        factory.set_slot_pblock(1, 1, slot_x1y1_ranges)

        return factory

    raise NotImplementedError(f"Platform {platform} is not supported")


def get_u50_default_schedule() -> ScheduleFactory:
    """Get a U50 default partition schedule."""
    return get_grid_one_iter_factory(2, 2)


if __name__ == "__main__":
    u50 = get_u50_default_device()
    with open("u50.json", "w", encoding="utf-8") as f:
        f.write(u50.model_dump_json(indent=2))
