"""Base project."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import json
import logging
import os
import shutil
from collections.abc import Iterable
from pathlib import Path

from rapidstream.assets.device.virtual_device import VirtualDevice
from rapidstream.assets.ui.common.commands import rapidstream_config
from rapidstream.assets.ui.common.impl import (
    paramterized_export_implementation_script,
    paramterized_export_project,
)
from rapidstream.assets.ui.common.structure import (
    CELL_PREASSIGN_CONFIG_PATH,
    EXPORTED_DESIGN_PATH,
    IMPORTED_JSON_PATH,
    IMPORTER_CONFIG_PATH,
    IMPORTER_LOG_PATH,
    PORT_PREASSIGN_CONFIG_PATH,
    create_project_dirs,
)
from rapidstream.assets.utilities.types import ImporterConfig
from rapidstream.assets.utilities.verilog import get_call_graph
from rapidstream.assets.utilities.vivado import get_clocks_max_frequency

_logger = logging.getLogger(__name__)


class RapidStreamBase:  # pylint: disable=too-many-instance-attributes
    """The base class for RapidStream projects.

    This class is used to build a RapidStream project in an imperative manner.  The
    resulting project can be handled by the RapidStream toolchain.

    It supports specifying the parameters of the project, such as the working directory
    for the RapidStream toolchain, the part number and the board name.  It can:

    (1) Specify the top-level module name.
    (2) Add source files such as verilog design files, HLS reports, blackbox files, XCI
        files and XCI files that are only for interface analysis.
    (3) Specify the flatten targets.
    (4) Specify the pre-assignments of the modules to the floorplanning regions.
    (5) Specify the clock constraints of the ports.

    Attributes:
        work_dir: The working directory for the RapidStream toolchain.
        part_num: The part number, such as "xcu250-figd2104-2L-e"
        board_name: The board name, such as "xilinx.com:au250:part0:1.3".

        top_module_name: The top-level module's module name.
        vlog_files: The paths to the Verilog files in the project.
        hls_report_dirs: the paths to the directories of HLS reports of the modules.
        blackbox_files: The paths to the blackbox files in the project.
        xci_files: The paths to the XCI files in the project.
        iface_only_xci_files: The paths to the the XCI files that are only for interface
            analysis in the project.

        flatten_targets: The targets to be flattened, specified by their module names.
        pre_assignments: The pre-assignments of the modules to the floorplanning regions.
        port_to_clock_period: The clock constraints of the ports.
    """

    work_dir: Path
    virtual_device: VirtualDevice

    top_module_name: str | None
    vlog_files: list[Path]
    hls_report_dirs: list[Path]
    blackbox_files: list[Path]
    xci_files: list[Path]
    iface_only_xci_files: list[Path]

    flatten_targets: list[str]
    cell_pre_assignments: dict[str, str]
    port_pre_assignments: dict[str, str]
    port_to_clock_period: dict[str, float]

    _last_pass_path: Path | None

    def __init__(
        self,
        work_dir: Path,
        virtual_device: VirtualDevice,
        reset: bool = False,
    ):
        """Initialize the rapidstream class.

        Args:
            work_dir: The working directory for the RapidStream toolchain.
            virtual_device: The virtual device for the project.
            reset: Whether to reset the results in the project from previous runs.
        """
        if reset:
            if work_dir.exists():
                shutil.rmtree(work_dir)
        else:
            _logger.info(f"Reusing results from previous runs in {work_dir}.")

        # Create the working directory
        create_project_dirs(work_dir)

        # Initialize the attributes
        self.work_dir = work_dir
        self.virtual_device = virtual_device

        with open(f"{work_dir}/virtual_device.json", "w", encoding="utf-8") as f:
            f.write(self.virtual_device.model_dump_json(indent=2))
        self.virtual_device_path = Path(f"{work_dir}/virtual_device.json")

        self.vlog_files = []
        self.blackbox_files = []
        self.xci_files = []
        self.hls_report_dirs = []
        self.flatten_targets = []
        self.iface_only_xci_files = []
        self.cell_pre_assignments = {}
        self.port_pre_assignments = {}
        self.port_to_clock_period = {}

        # dict from parent module to all its children modules
        self.call_graph: dict[str, set[str]] | None = None

        self._last_pass_path = None

    ############################
    #  Project configuration   #
    ############################

    def set_top_module_name(self, top_module_name: str) -> None:
        """Set the top-level module name."""
        self.top_module_name = top_module_name

        # top module will always be a flatten target
        self.add_flatten_targets([top_module_name])

    def add_vlog_files(self, vlog_files: list[Path]) -> None:
        """Add Verilog files to the project."""
        self._check_all_exists(vlog_files)
        self._check_all_file_extension(vlog_files, ".v")
        self.vlog_files += vlog_files

    def add_blackbox_files(self, blackbox_files: list[Path]) -> None:
        """Add black box files to the project."""
        self._check_all_exists(blackbox_files)
        self.blackbox_files += blackbox_files

    def add_xci_files(self, xci_files: list[Path]) -> None:
        """Add XCI files to the project."""
        self._check_all_exists(xci_files)
        self._check_all_file_extension(xci_files, ".xci")
        self.xci_files += xci_files

    def add_iface_only_xci_files(self, iface_only_xci_files: list[Path]) -> None:
        """Add XCI files that are only for interface analysis."""
        self._check_all_exists(iface_only_xci_files)
        self._check_all_file_extension(iface_only_xci_files, ".xci")
        self.iface_only_xci_files += iface_only_xci_files

    def add_hls_report_dirs(self, rpt_dirs: list[Path]) -> None:
        """Add HLS report directories."""
        self._check_all_exists(rpt_dirs)
        self._check_all_directories(rpt_dirs)
        self.hls_report_dirs += rpt_dirs

    def add_flatten_targets(self, flatten_targets: list[str]) -> None:
        """Add flatten targets."""
        self.flatten_targets += flatten_targets

    def get_flatten_targets_and_ancestors(self) -> set[str]:
        """Get all ancestor modules of the flatten targets, including the targets.

        Need to initialize call graph before calling this function.
        """
        assert self.call_graph is not None
        _logger.info("Mark all ancestors of existing flatten targets as group modules.")

        # Iterate until no new parents are found
        target_and_ancestors = set(self.flatten_targets)
        while True:
            parents = {
                parent
                for parent, children in self.call_graph.items()
                if children.intersection(target_and_ancestors)
            }
            if not (new_parents := parents - target_and_ancestors):
                break
            target_and_ancestors |= new_parents

        return target_and_ancestors

    def assign_port_to_region(
        self,
        port_name: str,
        target_region: str,
    ) -> None:
        """Constrain a port to a specific region of the FPGA.

        TODO: AutoBridge should check if the port is a top-level port. and this function
        should call it to perform the sanity check.
        """
        if port_name in self.port_pre_assignments:
            raise ValueError(f"Port {port_name} has already been assigned.")

        assert "/" not in port_name, "port name should not contain /"
        self.port_pre_assignments[port_name] = target_region

    def assign_port_to_region_test_mode(self) -> None:
        """Assign all ports to the same region for testing purposes."""
        self.assign_port_to_region(".*", "SLOT_X0Y0_To_SLOT_X0Y0")

    def assign_cell_to_region(self, pattern: str, target_region: str) -> None:
        """Constrain a cell to a specific region of the FPGA.

        Args:
            pattern: The pattern of the cell name in regexp.
            target_region: The target region. TODO: explain options and check validity.
        """
        assert not pattern.endswith("/"), "pattern should not end with /"
        self.cell_pre_assignments[pattern] = target_region

    def add_clock(self, port_name: str, period_ns: float) -> None:
        """Add a clock to the project."""
        self.port_to_clock_period[port_name] = period_ns

    ########################
    #  RapidStream Runner  #
    ########################

    def run(self) -> None:
        """Run the full RapidStream flow.

        This method should be overridden by the child class to suite different types.
        """
        self.import_project()
        self.export_project()
        self.export_implementation_script()

    def import_project(self) -> None:
        """Import the project."""
        if not self.port_pre_assignments:
            raise ValueError("No location constraints for top-level ports.")

        imported_pass_json_path = self.work_dir / IMPORTED_JSON_PATH
        if imported_pass_json_path.exists():
            _logger.info("Reusing the previous importer results.")
            return

        _logger.info(f"Saving pre-assignments to files")
        port_pre_assignments_json = self.work_dir / PORT_PREASSIGN_CONFIG_PATH
        port_pre_assignments_json.write_text(
            json.dumps(self.port_pre_assignments, indent=2)
        )

        cell_pre_assignments_json = self.work_dir / CELL_PREASSIGN_CONFIG_PATH
        cell_pre_assignments_json.write_text(
            json.dumps(self.cell_pre_assignments, indent=2)
        )

        rapidstream_config(
            config_json_path=self._generate_config_json(),
            imported_json_path=imported_pass_json_path,
            log_path=self.work_dir / IMPORTER_LOG_PATH,
            port_pre_assignments_json=port_pre_assignments_json,
        )

        assert os.path.isfile(imported_pass_json_path)
        self._last_pass_path = imported_pass_json_path

    def export_project(self, disable_syntax_check: bool = True) -> Path:
        """Export the transformed project."""
        if not self._last_pass_path:
            raise RuntimeError("The project has not been imported yet.")

        return paramterized_export_project(
            work_dir=self.work_dir,
            input_json_path=self._last_pass_path,
            port_to_clock_period=self.port_to_clock_period,
            disable_syntax_check=disable_syntax_check,
        )

    def export_implementation_script(self, run_impl: bool = True) -> Path:
        """Export the default implementation script for running the implementation."""
        self._drc_check()
        assert self.top_module_name
        return paramterized_export_implementation_script(
            work_dir=self.work_dir,
            top_module_name=self.top_module_name,
            part_num=self.virtual_device.part_num,
            board_name=self.virtual_device.board_name,
            run_impl=run_impl,
        )

    def get_clocks_max_frequency(self) -> dict[str, float]:
        """Get the maximum operating frequency for each clock of the project."""
        timing_report_path = self.work_dir / EXPORTED_DESIGN_PATH / "timing_summary.rpt"
        if not timing_report_path.exists():
            raise ValueError("The timing report does not exist.")
        return get_clocks_max_frequency(str(timing_report_path))

    def get_application_frequency(self) -> float:
        """Get the application clock's frequency of the project."""
        freqs = list(self.get_clocks_max_frequency().values())
        if len(freqs) != 1:
            raise NotImplementedError(
                "Please override this method to specify the application clock."
            )
        return freqs[0]

    #######################
    #  Utility functions  #
    #######################

    def _generate_config_json(self) -> Path:
        """Generate the config json for the project."""
        if not self.top_module_name:
            raise ValueError("The top-level module name is not specified.")

        self.call_graph = get_call_graph([str(f) for f in self.vlog_files])

        # Obtain the flatten targets and their ancestors in the call graph
        group_modules = self.get_flatten_targets_and_ancestors()
        _logger.debug(
            f"Flatten targets are {self.flatten_targets}. Their ancestor modules in the"
            " call graph are also marked as group modules:"
            f" {group_modules - set(self.flatten_targets)}"
        )
        if not group_modules:
            raise ValueError("Flatten targets must be specified")

        def canonicalized(paths: Iterable[Path]) -> tuple[str, ...]:
            return tuple(sorted({str(p.resolve()) for p in paths}))

        # Dump the importer config
        config = ImporterConfig(
            # Project parameters
            part_num=self.virtual_device.part_num,
            # Project sources
            top=self.top_module_name,
            rtl_sources=canonicalized(self.vlog_files + self.blackbox_files),
            hls_report_dirs=canonicalized(self.hls_report_dirs),
            xci_sources=canonicalized(self.xci_files),
            iface_only_xci_sources=canonicalized(self.iface_only_xci_files),
            # Deprecated parameters
            tcl_sources=(),
            hls_solution_dirs=(),
            # Project constraints
            rtl_group_modules=tuple(sorted(group_modules)),
        )
        config_json_path = self.work_dir / IMPORTER_CONFIG_PATH
        config_json_path.write_text(config.model_dump_json())

        return config_json_path

    def _drc_check(self) -> None:
        """Run DRC check for running the floorplanning flow."""
        if not self.port_to_clock_period:
            raise ValueError("Must add clocks.")
        if not self.port_pre_assignments:
            raise ValueError("No location constraints for top-level ports.")

    def get_latest_project(self) -> str:
        """Get the latest project."""
        if not self._last_pass_path:
            raise RuntimeError("The project has not been imported yet.")
        return self._last_pass_path.read_text()

    @staticmethod
    def _check_all_exists(paths: list[Path]) -> None:
        """Check if all files exist, otherwise raise ValueError."""
        for path in paths:
            if not path.exists():
                raise ValueError(f"Path {path} does not exist.")

    @staticmethod
    def _check_all_directories(paths: list[Path]) -> None:
        """Check if all paths are directories, otherwise raise ValueError."""
        for path in paths:
            if not path.is_dir():
                raise ValueError(f"Path {path} is not a directory.")

    @staticmethod
    def _check_all_file_extension(file_paths: list[Path], ext: str) -> None:
        """Check if all files has the extension, otherwise raise ValueError."""
        for file_path in file_paths:
            if not file_path.is_file():
                raise ValueError(f"Path {file_path} is not a file.")
            if file_path.suffix != ext:
                raise ValueError(f"File {file_path} does not have the {ext} extension.")
