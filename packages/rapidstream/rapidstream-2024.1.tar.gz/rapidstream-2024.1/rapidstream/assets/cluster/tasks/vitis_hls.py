"""Tasks to run Vitis HLS on the Dask cluster.

The duplication of tasks in this module is intentional. Each task is a separate function
to allow analysis of the run status on the Dask dashboard.
"""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

from pathlib import Path
from subprocess import CompletedProcess

from rapidstream.assets.cluster.task import task
from rapidstream.assets.cluster.util import run_command


@task
def run_vitis_hls_synth(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vitis HLS synthesis with the specified Tcl script."""
    return run_vitis_hls(tcl, cwd, targs, as_bytes, timeout)


@task
def run_vitis_hls_cosim_gen(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vitis HLS with the specified Tcl script to generate cosimulation files."""
    return run_vitis_hls(tcl, cwd, targs, as_bytes, timeout)


@task
def run_vitis_hls(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vitis HLS with the specified Tcl script."""
    return run_command(
        args=(
            [
                "vitis_hls",
                str(tcl),
                *(["-tclargs", *targs] if targs else []),
            ]
        ),
        cwd=cwd,
        as_bytes=as_bytes,
        timeout=timeout,
    )
