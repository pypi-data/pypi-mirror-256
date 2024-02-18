"""Tasks to run simulations on the Dask cluster.

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
def run_xsim_script(
    args: list[str], cwd: Path, as_bytes: int | None = None, timeout: int | None = None
) -> CompletedProcess[bytes]:
    """Run a script to invoke XSim for simulation."""
    return run_command(args, cwd, as_bytes, timeout)


@task
def run_post_cosim_program(
    args: list[str], cwd: Path, as_bytes: int | None = None, timeout: int | None = None
) -> CompletedProcess[bytes]:
    """Run a post-cosimulation program."""
    return run_command(args, cwd, as_bytes, timeout)
