"""Base project."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import logging
import shutil
from pathlib import Path

from rapidstream.assets.device.virtual_device import VirtualDevice
from rapidstream.assets.ui.common.structure import GENERATED_PATH
from rapidstream.assets.ui.core import RapidStreamCore
from rapidstream.assets.utilities.autopilot import (
    AutoPilotParser,
    is_dataflow_module_above_area,
)
from rapidstream.assets.utilities.vivado import generate_xci_from_tcl

_logger = logging.getLogger(__name__)

HLS_XCI_PATH = GENERATED_PATH / "hls_xci"


class RapidStreamHLS(RapidStreamCore):
    """The HLS flow of RapidStream.

    This class is used to run the RapidStream flow for HLS projects.

    In addition to the functions in RapidStreamCore, this class provides the following:

    (1) It will automatically add the part number from the HLS solution.
    (2) It will automatically add the top-level module name from the HLS solution.
    (3) It will automatically add the clock period from the HLS solution.
    (4) It will generate XCI files from HLS TCL IP files and add them into the project.
    (5) It will infer dataflow modules from HLS reports and add them into flatten targets.

    Attributes:
        hls_xci_dir: Directory to store XCI files generated from HLS TCL files.
    """

    hls_xci_dir: Path

    def __init__(
        self,
        work_dir: Path,
        virtual_device: VirtualDevice,
        reset: bool = False,
        hls_flatten_threshold: float = 5,
    ):
        """Initialize the rapidstream class.

        area_threshold: Minimum estimated usage percentage to infer an HLS module as
                dataflow.
        """
        super().__init__(work_dir, virtual_device, reset)

        # Create the HLS XCI directory
        self.hls_xci_dir = self.work_dir / HLS_XCI_PATH
        if self.hls_xci_dir.exists() and reset:
            shutil.rmtree(self.hls_xci_dir)
        self.hls_xci_dir.mkdir(parents=True, exist_ok=True)

        self.hls_flatten_threshold = hls_flatten_threshold

    def config_from_hls_solution(self, hls_solution_path: Path) -> None:
        """Add an entire HLS solution to the project and set as top.

        This function will automatically import the HLS solution and set project params.
        """
        # (1) Parse the HLS solution to get the part number
        parser = AutoPilotParser(str(hls_solution_path))

        # (2) Parse the HLS solution to get the top-level module name
        self.set_top_module_name(parser.get_top_module())

        # (3) Parse the HLS solution to get the clock period
        self.add_clock(*parser.get_clock())

        self.add_hls_solution(hls_solution_path)

    def add_hls_solution(self, hls_solution_path: Path) -> None:
        """Add an entire HLS solution to the project.

        This function will automatically infer dataflow modules from HLS reports
        and add them into flatten targets.
        """
        if not hls_solution_path.is_dir():
            raise ValueError(f"{hls_solution_path} is not a directory.")

        _logger.info(f"Adding HLS solution: {hls_solution_path}")

        # FIXME: store the hls solution path in a global constants file
        self.add_hls_report_dirs([hls_solution_path / "syn" / "report"])

        # HLS may generate .dat files or other formats, which treats as blackboxes.
        source_path = hls_solution_path / "syn" / "verilog"
        files = tuple(p for p in source_path.rglob("*") if p.is_file())

        # Add all .v files to the project
        self.add_vlog_files([f for f in files if f.suffix == ".v"])

        # Add all blackbox files to the project
        self.add_blackbox_files([f for f in files if f.suffix not in {".v", ".tcl"}])

        # Generate XCI files from HLS TCL IP files
        tcl_files = [f for f in files if f.suffix == ".tcl"]
        self.add_hls_tcl_ip_file(tcl_files)

        _logger.info(f"Finished add HLS solution {hls_solution_path}")

    def get_flatten_targets_and_ancestors(self) -> set[str]:
        """Infer HLS flatten targets and then get all ancestors."""
        assert self.call_graph is not None
        self.infer_hls_dataflow_modules(set(self.call_graph.keys()))
        return super().get_flatten_targets_and_ancestors()

    def infer_hls_dataflow_modules(self, module_names: set[str]) -> None:
        """Infer dataflow modules from HLS reports and add to flatten targets."""
        assert self.vlog_files

        df_modules = []
        for module in module_names:
            if any(
                is_dataflow_module_above_area(
                    module, str(rpt_dir), self.hls_flatten_threshold
                )
                for rpt_dir in self.hls_report_dirs
            ):
                df_modules.append(module)

        df_modules = list(set(df_modules))
        _logger.info(
            f"Inferred HLS dataflow modules with at least {self.hls_flatten_threshold}%"
            f" estimated usage: {df_modules}"
        )

        self.add_flatten_targets(df_modules)

    def add_hls_tcl_ip_file(self, ip_tcls: list[Path]) -> None:
        """Generate and store XCI files from HLS TCL IP files."""
        generate_xci_from_tcl(
            [str(p) for p in ip_tcls],
            self.virtual_device.part_num,
            str(self.hls_xci_dir),
        )
        self.add_xci_files(list(self.hls_xci_dir.rglob("*.xci")))
        self.add_blackbox_files(ip_tcls)
