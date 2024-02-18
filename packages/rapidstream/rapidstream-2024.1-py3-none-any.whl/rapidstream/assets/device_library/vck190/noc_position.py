"""Record the NoC positions."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

from collections import namedtuple

XyPair = namedtuple("XyPair", "x y")

# map from NOC_NUM512 to clock region (x, y)
VCK190_NOC_TO_CR = {
    "NOC_NMU512_X0Y6": XyPair(1, 4),
    "NOC_NMU512_X1Y6": XyPair(3, 4),
    "NOC_NMU512_X2Y6": XyPair(5, 4),
    "NOC_NMU512_X3Y6": XyPair(7, 4),
    "NOC_NMU512_X0Y5": XyPair(1, 3),
    "NOC_NMU512_X1Y5": XyPair(3, 3),
    "NOC_NMU512_X2Y5": XyPair(5, 3),
    "NOC_NMU512_X3Y5": XyPair(7, 3),
    "NOC_NMU512_X0Y4": XyPair(1, 3),
    "NOC_NMU512_X1Y4": XyPair(3, 3),
    "NOC_NMU512_X2Y4": XyPair(5, 3),
    "NOC_NMU512_X3Y4": XyPair(7, 3),
    "NOC_NMU512_X0Y3": XyPair(1, 2),
    "NOC_NMU512_X1Y3": XyPair(3, 2),
    "NOC_NMU512_X2Y3": XyPair(5, 2),
    "NOC_NMU512_X3Y3": XyPair(7, 2),
    "NOC_NMU512_X0Y2": XyPair(1, 2),
    "NOC_NMU512_X1Y2": XyPair(3, 2),
    "NOC_NMU512_X2Y2": XyPair(5, 2),
    "NOC_NMU512_X3Y2": XyPair(7, 2),
    "NOC_NMU512_X0Y1": XyPair(1, 1),
    "NOC_NMU512_X1Y1": XyPair(3, 1),
    "NOC_NMU512_X2Y1": XyPair(5, 1),
    "NOC_NMU512_X3Y1": XyPair(7, 1),
    "NOC_NMU512_X0Y0": XyPair(1, 1),
    "NOC_NMU512_X1Y0": XyPair(3, 1),
    "NOC_NMU512_X2Y0": XyPair(5, 1),
    "NOC_NMU512_X3Y0": XyPair(7, 1),
}


VCK190_DEFAULT_CR_TO_SLOT = {}

for x in range(0, 5):
    for y in range(1, 3):
        VCK190_DEFAULT_CR_TO_SLOT[XyPair(x, y)] = "SLOT_X0Y0_To_SLOT_X0Y0"

for x in range(5, 10):
    for y in range(1, 3):
        VCK190_DEFAULT_CR_TO_SLOT[XyPair(x, y)] = "SLOT_X1Y0_To_SLOT_X1Y0"

for x in range(0, 5):
    for y in range(3, 5):
        VCK190_DEFAULT_CR_TO_SLOT[XyPair(x, y)] = "SLOT_X0Y1_To_SLOT_X0Y1"

for x in range(5, 10):
    for y in range(3, 5):
        VCK190_DEFAULT_CR_TO_SLOT[XyPair(x, y)] = "SLOT_X1Y1_To_SLOT_X1Y1"


def get_vck190_slot_name_from_noc_name(noc_name: str) -> str:
    """Get the slot name from the noc name."""
    return VCK190_DEFAULT_CR_TO_SLOT[VCK190_NOC_TO_CR[noc_name]]
