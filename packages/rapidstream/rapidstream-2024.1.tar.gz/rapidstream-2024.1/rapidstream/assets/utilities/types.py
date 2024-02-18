"""The type definitions of RapidStream's utilities and configurations."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import os

from pydantic import BaseModel


class ImporterConfig(BaseModel):
    """The input to the importer."""

    hls_solution_dirs: tuple[str, ...]
    rtl_sources: tuple[str, ...]
    rtl_group_modules: tuple[str, ...]
    xci_sources: tuple[str, ...]
    iface_only_xci_sources: tuple[str, ...]
    tcl_sources: tuple[str, ...]
    hls_report_dirs: tuple[str, ...]
    part_num: str | None
    top: str

    def __init__(self, **data: object) -> None:
        """Initialize the ImporterConfig."""
        super().__init__(**data)

        assert all(os.path.isdir(path) for path in self.hls_solution_dirs)
        assert all(os.path.isfile(path) for path in self.rtl_sources)
        assert all(os.path.isfile(path) for path in self.xci_sources)
        assert all(os.path.isfile(path) for path in self.iface_only_xci_sources)
        assert all(os.path.isfile(path) for path in self.tcl_sources)
        assert all(os.path.isdir(path) for path in self.hls_report_dirs)
