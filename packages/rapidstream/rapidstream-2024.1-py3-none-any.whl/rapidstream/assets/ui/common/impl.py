"""Utilities for RapidStream to run implementations and design space exploration."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import json
import logging
import shutil
from pathlib import Path

from jinja2 import Template

from rapidstream.assets.ui.common.commands import (
    add_pipeline,
    pblock_gen,
    rapidstream_autobridge,
    rapidstream_exporter,
)
from rapidstream.assets.ui.common.structure import (
    CELL_PREASSIGN_CONFIG_PATH,
    DSE_ADD_PIPELINE_LOG_PATH,
    DSE_ADD_PIPELINE_PATH,
    DSE_CANDIDATE_PATH,
    DSE_LOG_PATH,
    DSE_PATH,
    EXPORTED_DESIGN_PATH,
    EXPORTED_IMPL_PATH,
    EXPORTED_XDC_PATH,
    EXPORTER_LOG_PATH,
    EXPORTER_XDC_CLOCKS_PATH,
    EXPORTER_XDC_FLOORPLAN_PATH,
    PBLOCK_GEN_LOG_PATH,
    PORT_PREASSIGN_CONFIG_PATH,
    create_project_dirs,
)

_logger = logging.getLogger(__name__)


RE_NO_VALID_FLOORPLAN = "No valid floorplan found."

I_CREATE_DEFAULT_IMPL = "Creating the default implementation..."
I_WRITE_TCL = 'Writing the implementation script to "%s"...'


def prepare_autobridge_dse(
    input_json_path: Path,
    work_dir: Path,
    device_config: Path | None,
) -> tuple[Path, ...]:
    """Run the autobridge pass to prepare DSE candidates."""
    rapidstream_autobridge(
        input_json_path=input_json_path,
        output_json_path=None,
        log_path=work_dir / DSE_LOG_PATH,
        port_pre_assignments_json=work_dir / PORT_PREASSIGN_CONFIG_PATH,
        cell_pre_assignments_json=work_dir / CELL_PREASSIGN_CONFIG_PATH,
        device_config=device_config,
        run_dse=True,
        dse_dir=work_dir / DSE_PATH,
    )

    if not (candidates := tuple((work_dir / DSE_PATH).rglob("*.json"))):
        raise RuntimeError(RE_NO_VALID_FLOORPLAN)

    return candidates


def add_pipeline_to_candidate(
    idx: int,
    post_autobridge_ir_path: Path,
    work_dir: Path,
    device_config_path: Path,
) -> tuple[Path, Path]:
    """Process the DSE candidate and generate the implementation script."""
    local_dir = work_dir / DSE_PATH / DSE_CANDIDATE_PATH.format(idx=idx)
    local_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(post_autobridge_ir_path, local_dir)

    create_project_dirs(local_dir)

    add_pipeline_json = local_dir / DSE_ADD_PIPELINE_PATH

    add_pipeline(
        input_json_path=local_dir / post_autobridge_ir_path.name,
        output_json_path=add_pipeline_json,
        log_path=local_dir / DSE_ADD_PIPELINE_LOG_PATH,
        device_config=device_config_path,
    )

    return local_dir, add_pipeline_json


def export_candidate(
    local_dir: Path,
    add_pipeline_json: Path,
    port_to_clock_period: dict[str, float],
    top_module_name: str,
    part_num: str,
    board_name: str | None,
) -> tuple[Path, Path]:
    """Process the DSE candidate and generate the implementation script."""
    paramterized_export_project(
        work_dir=local_dir,
        input_json_path=add_pipeline_json,
        port_to_clock_period=port_to_clock_period,
        disable_syntax_check=True,
    )

    assert top_module_name is not None
    impl_tcl = paramterized_export_implementation_script(
        work_dir=local_dir,
        top_module_name=top_module_name,
        part_num=part_num,
        board_name=board_name,
        run_impl=True,
    )

    return local_dir, impl_tcl


def paramterized_export_project(
    work_dir: Path,
    input_json_path: Path,
    port_to_clock_period: dict[str, float],
    disable_syntax_check: bool,
) -> Path:
    """Internal utility to export the project."""
    # Export the project design
    rapidstream_exporter(
        project_json_path=input_json_path,
        design_path=work_dir / EXPORTED_DESIGN_PATH,
        log_path=work_dir / EXPORTER_LOG_PATH,
        disable_syntax_check=disable_syntax_check,
    )

    # Export floorplan constraints
    project = json.loads(input_json_path.read_text())
    if project["island_to_pblock_range"]:
        pblock_gen(
            input_json_path=input_json_path,
            log_path=work_dir / PBLOCK_GEN_LOG_PATH,
            output_tcl=work_dir / EXPORTER_XDC_FLOORPLAN_PATH,
        )

    # Export clock constraints
    with open(work_dir / EXPORTER_XDC_CLOCKS_PATH, "w", encoding="utf-8") as f:
        for port, period_ns in port_to_clock_period.items():
            f.write(f"create_clock -period {period_ns} [get_ports {port}]\n")

    return work_dir / EXPORTED_DESIGN_PATH


def paramterized_export_implementation_script(
    work_dir: Path,
    top_module_name: str,
    part_num: str,
    board_name: str | None,
    run_impl: bool,
) -> Path:
    """Internal utility to export the default implementation script."""
    return Path(
        setup_ooc_run(
            run_impl=run_impl,
            top=top_module_name,
            src_dir=str(work_dir / EXPORTED_DESIGN_PATH),
            pblock_dir=str(work_dir / EXPORTED_XDC_PATH),
            synth_dir=str(work_dir / EXPORTED_IMPL_PATH),
            part_num=part_num,
            board_name=board_name,
        )
    )


def setup_ooc_run(
    synth_dir: str,
    top: str,
    part_num: str,
    src_dir: str,
    pblock_dir: str,
    run_impl: bool,
    user_xdc_dir: str | None = None,
    board_name: str | None = None,
) -> str:
    """Create a default implementation script for out-of-context runs."""
    _logger.info(I_CREATE_DEFAULT_IMPL)

    tcl = Template(
        r"""
proc getEnvInt { varName defaultIntValue } {
    set value [expr {[info exists ::env($varName)] ? $::env($varName) : $defaultIntValue}]
    return [expr {int($value)}]
}

create_project -force ./vivado/project -part {{ part_num }}

{% if board_name %}
set_property board_part {{ board_name }} [current_project]
{% endif %}

set ip_files [glob -nocomplain {{ src_dir }}/*/*.xci]
if {[llength $ip_files] > 0} {
    import_ip $ip_files
}
import_files {{ src_dir }}
import_files -fileset constrs_1 {{ pblock_dir }}
upgrade_ip -quiet [get_ips *]
generate_target synthesis [ get_files *.xci ]
set_property top {{ top }} [current_fileset]
set_property top {{ top }} [current_fileset]
set_property -name {STEPS.SYNTH_DESIGN.ARGS.MORE OPTIONS} -value {-mode out_of_context} -objects [get_runs synth_1]

{% if user_xdc_dir %}
import_files -fileset constrs_1 {{ user_xdc_dir }}
{% endif %}

launch_runs synth_1 -jobs [getEnvInt "VIVADO_SYNTH_JOBS" 8]
wait_on_run synth_1
open_run synth_1
write_checkpoint synth.dcp
reset_timing
write_checkpoint synth_no_clock.dcp
open_checkpoint synth.dcp

foreach pblock [get_pblocks *] {
    set cells [get_cells -of_objects $pblock]
    if {[llength $cells] == 0} {
        puts "CRITICAL WARNING: pblock $pblock is empty."
        delete_pblock $pblock
    }
}

{% if run_impl %}
opt_design
place_design
phys_opt_design
write_checkpoint place.dcp
route_design
phys_opt_design
write_checkpoint route.dcp
report_timing_summary -file timing_summary.rpt
{% endif %}
    """  # noqa: B950
    ).render(
        synth_dir=synth_dir,
        top=top,
        part_num=part_num,
        src_dir=src_dir,
        pblock_dir=pblock_dir,
        run_impl=run_impl,
        user_xdc_dir=user_xdc_dir,
        board_name=board_name,
    )

    tcl_path = f"{synth_dir}/synth.tcl"
    _logger.info(I_WRITE_TCL, tcl_path)
    with open(tcl_path, "w", encoding="utf-8") as f:
        f.write(tcl)

    return tcl_path
