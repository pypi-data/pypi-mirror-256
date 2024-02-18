"""Tasks to run Vivado on the Dask cluster.

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
def run_vivado_vhdl_to_verilog(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado with the specified Tcl script to convert VHDL to Verilog."""
    return run_vivado(tcl, cwd, targs, log_file, journal_file, as_bytes, timeout)


@task
def run_vivado_xci_generation(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado with the specified Tcl script to generate XCI files."""
    return run_vivado(tcl, cwd, targs, log_file, journal_file, as_bytes, timeout)


@task
def run_vivado_analyze(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado with the specified Tcl script to analyze the design."""
    return run_vivado(tcl, cwd, targs, log_file, journal_file, as_bytes, timeout)


@task
def run_vivado_elab(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado elaboration with the specified Tcl script."""
    return run_vivado(tcl, cwd, targs, log_file, journal_file, as_bytes, timeout)


@task
def run_vivado_synth(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado synthesis with the specified Tcl script."""
    return run_vivado(tcl, cwd, targs, log_file, journal_file, as_bytes, timeout)


@task
def run_vivado_impl(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado implementation with the specified Tcl script."""
    return run_vivado(tcl, cwd, targs, log_file, journal_file, as_bytes, timeout)


@task
def run_vivado_link(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado with the specified Tcl script to link the design."""
    return run_vivado(tcl, cwd, targs, log_file, journal_file, as_bytes, timeout)


@task
def run_vivado_cosim(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado cosimulation with the specified Tcl script."""
    return run_vivado(tcl, cwd, targs, log_file, journal_file, as_bytes, timeout)


@task
def run_vivado(
    tcl: Path,
    cwd: Path,
    targs: tuple[str] | list[str] | None = None,
    log_file: Path | None = None,
    journal_file: Path | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Run Vivado with the specified Tcl script."""
    return run_command(
        args=[
            "vivado",
            "-mode",
            "batch",
            "-source",
            str(tcl),
            *(["-log", str(log_file)] if log_file else []),
            *(["-journal", str(journal_file)] if journal_file else []),
            *(["-tclargs", *targs] if targs else []),
        ],
        cwd=cwd,
        as_bytes=as_bytes,
        timeout=timeout,
    )
