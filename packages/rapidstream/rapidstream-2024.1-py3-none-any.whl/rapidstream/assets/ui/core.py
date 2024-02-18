"""Base project."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import concurrent.futures
import logging
from pathlib import Path

from rapidstream.assets.cluster.tasks.vivado import run_vivado_impl
from rapidstream.assets.cluster.util import check_async_command, check_async_commands
from rapidstream.assets.device.virtual_device import VirtualDevice
from rapidstream.assets.ui.base import RapidStreamBase
from rapidstream.assets.ui.common.commands import (
    add_pipeline,
    flatten,
    get_area,
    rapidstream_autobridge,
    split_aux,
)
from rapidstream.assets.ui.common.impl import (
    add_pipeline_to_candidate,
    export_candidate,
    prepare_autobridge_dse,
)
from rapidstream.assets.ui.common.passes import Pass
from rapidstream.assets.ui.common.structure import (
    CELL_PREASSIGN_CONFIG_PATH,
    DSE_PATH,
    EXPORTED_DESIGN_PATH,
    GET_AREA_PATH,
    PORT_PREASSIGN_CONFIG_PATH,
    SPLIT_AUX_PATH,
    get_pass_json_rel_path,
    get_pass_log_rel_path,
)

_logger = logging.getLogger(__name__)


class RapidStreamCore(RapidStreamBase):  # pylint: disable=too-many-instance-attributes
    """The core flow for RapidStream projects.

    This class is used to run the core flow for RapidStream projects using the
    RapidStream toolchain.  It can be inherited to create custom flows for different
    source types, such as HLS or Vitis projects.

    This class provides the following functionality in addition to the base class:

    (1) Run the transform passes to generate the optimized RapidStream IR.
    (2) Perform design space exploration (DSE) to find the best pipeline configuration.
    """

    _last_pass_id: int = 0

    def __init__(
        self,
        work_dir: Path,
        virtual_device: VirtualDevice,
        reset: bool = False,
    ) -> None:
        """Initialize the RapidStreamCore class."""
        self._last_pass_id = 0
        super().__init__(work_dir, virtual_device, reset)

    #########################
    #  RapidStream Methods  #
    #########################

    def run(self, run_impl: bool = True) -> None:
        """Execute the full RapidStream flow."""
        self.import_project()

        self._drc_check()
        self.run_passes()

        self.export_project()

        exported_design_dir = self.work_dir / EXPORTED_DESIGN_PATH
        exported_tcl_path = self.export_implementation_script(run_impl)
        check_async_command(
            run_vivado_impl.submit(exported_tcl_path, exported_design_dir)
        )

    def run_passes(self) -> None:
        """Run all passes."""
        self.run_passes_before(None)

    def run_passes_before(self, pass_name: str | None) -> None:
        """Run all passes before the given pass name."""
        for pass_func in self.get_passes():
            if pass_func.name == pass_name:
                break
            self.run_pass(pass_func)

    def run_dse(self) -> None:
        """Run pre-autobridge passes and then perform DSE on AutoBridge.

        Implement each candidate solution in OOC mode.
        """
        work_dir_to_ir = self.run_dse_until_add_pipeline()

        # export
        work_dir_to_ooc_tcl = self.parallel_export_candidates(work_dir_to_ir)

        # vivado impl
        self.launch_parallel_impl(work_dir_to_ooc_tcl)

    def run_dse_until_add_pipeline(self) -> dict[Path, Path]:
        """Run pre-autobridge passes and then perform DSE on AutoBridge.

        Implement each candidate solution in OOC mode.
        """
        # import, split-aux, flatten, get-area
        self.run_pre_autobridge()
        assert self._last_pass_path is not None

        # run multiple autobridge with different parameters
        _logger.info("Running DSE...")
        candidates = prepare_autobridge_dse(
            input_json_path=self._last_pass_path,
            work_dir=self.work_dir,
            device_config=self.virtual_device_path,
        )

        # add-pipeline
        return self.run_parallel_add_pipeline(candidates)

    def run_pre_autobridge(self) -> None:
        """Run pre-autobridge passes."""
        self._drc_check()

        _logger.info("Importing project...")
        self.import_project()

        # Run pre-autobridge passes
        _logger.info("Running pre-autobridge passes...")
        for p in self.get_passes():
            if p.name == "autobridge":
                break
            self.run_pass(p)

    def run_parallel_add_pipeline(
        self, candidates: tuple[Path, ...]
    ) -> dict[Path, Path]:
        """Run add pipeline pass for each candidate in parallel and export."""
        _logger.info("Running add pipeline pass...")
        assert self.top_module_name is not None
        work_dir_to_ir: dict[Path, Path] = {}
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Create a list of futures
            futures = [
                executor.submit(
                    add_pipeline_to_candidate,
                    idx,
                    candidate,
                    self.work_dir / DSE_PATH,
                    self.virtual_device_path,
                )
                for idx, candidate in enumerate(candidates)
            ]

            # As each future completes, update the dictionary
            for future in concurrent.futures.as_completed(futures):
                local_dir, add_pipeline_json = future.result()
                work_dir_to_ir[local_dir] = add_pipeline_json

        return work_dir_to_ir

    def parallel_export_candidates(
        self, work_dir_to_ir: dict[Path, Path]
    ) -> dict[Path, Path]:
        """Export the candidates."""
        work_dir_to_tcl: dict[Path, Path] = {}
        assert self.top_module_name is not None
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Create a list of futures
            futures = [
                executor.submit(
                    export_candidate,
                    local_dir,
                    post_pp_ir,
                    self.port_to_clock_period,
                    self.top_module_name,
                    self.virtual_device.part_num,
                    self.virtual_device.board_name,
                )
                for local_dir, post_pp_ir in work_dir_to_ir.items()
            ]

            # As each future completes, update the dictionary
            for future in concurrent.futures.as_completed(futures):
                local_dir, impl_tcl = future.result()
                work_dir_to_tcl[local_dir] = impl_tcl

        return work_dir_to_tcl

    def launch_parallel_impl(self, work_dir_to_tcl: dict[Path, Path]) -> None:
        """Launch parallel vivado implementation."""
        _logger.info("Launching parallel vivado implementation...")
        jobs = [
            run_vivado_impl.submit(tcl, work_dir)
            for work_dir, tcl in work_dir_to_tcl.items()
        ]
        check_async_commands(jobs)

    #####################
    #  Utility Methods  #
    #####################

    def get_passes(self, hls_cosim: bool = False) -> tuple[Pass, ...]:
        """Return the tuple of passes that needs to be run by their order."""
        return (
            Pass(
                name="split_aux",
                func=split_aux,
                work_dir=self.work_dir / SPLIT_AUX_PATH,
            ),
            Pass(
                name="flatten",
                func=flatten,
            ),
            Pass(
                name="get_area",
                func=get_area,
                part_num=self.virtual_device.part_num,
                board_name=self.virtual_device.board_name,
                work_dir=self.work_dir / GET_AREA_PATH,
            ),
            Pass(
                name="autobridge",
                func=rapidstream_autobridge,
                port_pre_assignments_json=self.work_dir / PORT_PREASSIGN_CONFIG_PATH,
                cell_pre_assignments_json=self.work_dir / CELL_PREASSIGN_CONFIG_PATH,
                device_config=self.virtual_device_path,
            ),
            Pass(
                name="add_pipeline",
                func=add_pipeline,
                device_config=self.virtual_device_path,
                hls_cosim=hls_cosim,
            ),
        )

    def run_pass(self, the_pass: Pass) -> None:
        """Run a transform pass and return the project."""
        if self._last_pass_path is None:
            raise RuntimeError("The project has not been imported yet.")

        # Get the pass ID
        self._last_pass_id += 1
        pass_id = self._last_pass_id

        # Resolve the paths for the pass
        pass_json_path = self.work_dir / get_pass_json_rel_path(pass_id, the_pass.name)
        pass_log_path = self.work_dir / get_pass_log_rel_path(pass_id, the_pass.name)

        # If the pass has already been run, then skip it
        if not pass_json_path.exists():
            # Otherwise, run the pass
            the_pass(
                input_json_path=self._last_pass_path,
                output_json_path=pass_json_path,
                log_path=pass_log_path,
            )

        # Record the path to the last pass for the next run
        self._last_pass_path = pass_json_path
