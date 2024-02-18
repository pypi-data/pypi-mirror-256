"""The interface to the RapidStream proprietary commands."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import logging
import subprocess
import time
from pathlib import Path

_logger = logging.getLogger(__name__)

I_RUNNING_COMMAND_LOG_FILE = 'Running command: "%s"...\nLog file: "%s".'
RE_COMMAND_FAILED = 'Command "{command}" failed, see log file "{log}" for details.'

###############################################
#  Direct Access to the RapidStream commands  #
###############################################


def rapidstream_config(
    config_json_path: Path,
    imported_json_path: Path,
    log_path: Path,
    port_pre_assignments_json: Path,
    verbose: bool = True,
) -> None:
    """Run the rapidstream-config command."""
    cmd = [
        "rapidstream-config",
        "--config-file",
        str(config_json_path),
        "--output-file",
        str(imported_json_path),
        *(["-vvv"] if verbose else []),
        "--port-pre-assignments-json",
        str(port_pre_assignments_json),
    ]
    run_cmd_with_live_log(cmd, str(config_json_path.parent), str(log_path))


def rapidstream_exporter(
    project_json_path: Path,
    design_path: Path,
    log_path: Path,
    verbose: bool = True,
    disable_syntax_check: bool = True,
) -> None:
    """Run the rapidstream-config command."""
    cmd = [
        "rapidstream-exporter",
        "-i",
        str(project_json_path),
        "-f",
        str(design_path),
    ]

    if disable_syntax_check:
        cmd.append("--disable-syntax-check")

    if verbose:
        cmd.append("-vvv")

    run_cmd_with_live_log(cmd, str(design_path), str(log_path))


def rapidstream_optimizer(
    project_json_path: Path,
    output_json_path: Path,
    log_path: Path,
    pass_name: str,
    args: tuple[str, ...] = (),
    verbose: bool = True,
) -> None:
    """Run the rapidstream-optimizer command."""
    cmd = [
        "rapidstream-optimizer",
        "-i",
        str(project_json_path),
        "-o",
        str(output_json_path),
        *(["-vvv"] if verbose else []),
        pass_name,
        *args,
    ]
    run_cmd_with_live_log(cmd, str(output_json_path.parent), str(log_path))


def rapidstream_autobridge(
    input_json_path: Path,
    output_json_path: Path | None,
    log_path: Path,
    port_pre_assignments_json: Path,
    cell_pre_assignments_json: Path | None,
    device_config: Path | None = None,
    run_dse: bool = False,
    dse_dir: Path | None = None,
    verbose: bool = True,
) -> None:
    """Run the autbridge pass."""
    args = [f"--port-pre-assignments={port_pre_assignments_json}"]
    if cell_pre_assignments_json:
        args.append(f"--cell-pre-assignments={cell_pre_assignments_json}")
    if device_config:
        args.append(f"--device-config={device_config}")
    if run_dse:
        args.append("--run-dse")
    if dse_dir:
        args.append(f"--dse-dir={dse_dir}")

    cmd = [
        "rapidstream-autobridge",
        *("-i", str(input_json_path)),
        *(("-o", str(output_json_path)) if output_json_path else ()),
        *(("-vvv",) if verbose else ()),
        *args,
    ]
    run_cmd_with_live_log(cmd, str(input_json_path.parent), str(log_path))


###################################################
#  Access to the RapidStream optimization passes  #
###################################################


def split_aux(
    input_json_path: Path,
    output_json_path: Path,
    log_path: Path,
    work_dir: Path | None,
) -> None:
    """Run the split aux pass."""
    args = []
    if work_dir:
        args.append(f"--work-dir={work_dir}")

    rapidstream_optimizer(
        input_json_path,
        output_json_path,
        log_path,
        "split-aux",
        tuple(args),
    )


def flatten(
    input_json_path: Path,
    output_json_path: Path,
    log_path: Path,
) -> None:
    """Run the flatten pass."""
    rapidstream_optimizer(
        input_json_path,
        output_json_path,
        log_path,
        "flatten",
    )


def get_area(
    input_json_path: Path,
    output_json_path: Path,
    log_path: Path,
    part_num: str | None = None,
    board_name: str | None = None,
    work_dir: Path | None = None,
) -> None:
    """Run the get area pass."""
    if not part_num and not board_name:
        raise ValueError("Either part_num or board_name must be set.")

    args = []
    if part_num:
        args.append(f"--part-num={part_num}")
    if board_name:
        args.append(f"--board-name={board_name}")
    if work_dir:
        args.append(f"--work-dir={work_dir}")

    rapidstream_optimizer(
        input_json_path,
        output_json_path,
        log_path,
        "get-area",
        args=tuple(args),
    )


def add_pipeline(
    input_json_path: Path,
    output_json_path: Path,
    log_path: Path,
    device_config: Path | None,
    hls_cosim: bool | None = None,
) -> None:
    """Run the add pipeline pass."""
    args = []
    if device_config:
        args.append(f"--device-config={device_config}")
    if hls_cosim is not None:
        args.append(f"--hls-cosim={hls_cosim}")

    rapidstream_optimizer(
        input_json_path,
        output_json_path,
        log_path,
        "add-pipeline",
        args=tuple(args),
    )


def pblock_gen(
    input_json_path: Path,
    log_path: Path,
    output_tcl: Path,
    user_pblock_name: str | None = None,
) -> None:
    """Run the add pipeline pass."""
    args = [f"--output-tcl={output_tcl}"]
    if user_pblock_name:
        args.append(f"--user-pblock-name={user_pblock_name}")

    rapidstream_optimizer(
        input_json_path,
        Path("/dev/null"),
        log_path,
        "pblock-gen",
        args=tuple(args),
    )


################################################
#  Utility functions for running the commands  #
################################################


def run_cmd_with_live_log(cmd: list[str], work_dir: str, output_log: str) -> None:
    """Run the command with real-time updated log, which flushes to file every second."""
    _logger.info(I_RUNNING_COMMAND_LOG_FILE, " ".join(cmd), output_log)

    with (
        open(output_log, "w", encoding="utf-8") as f,
        subprocess.Popen(
            cmd,
            cwd=work_dir,
            stdout=f,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # line buffer
        ) as proc,
    ):
        # Flush the log file every second until the process is done
        while proc.poll() is None:
            f.flush()
            time.sleep(1)

        # Flush the log file one last time
        f.flush()
        return_code = proc.wait()

    if return_code != 0:
        with open(output_log, "r", encoding="utf-8") as f:
            _logger.error(f.read())
        raise RuntimeError(
            RE_COMMAND_FAILED.format(command=" ".join(cmd), log=output_log)
        )
