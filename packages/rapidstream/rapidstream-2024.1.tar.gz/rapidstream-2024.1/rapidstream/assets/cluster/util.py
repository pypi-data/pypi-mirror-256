"""Common utility tasks for the Dask cluster."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""


import atexit
import logging
import os
import resource
import tempfile
import threading
from subprocess import PIPE, CompletedProcess, Popen, TimeoutExpired
from typing import IO

from psutil import Process

from rapidstream.assets.cluster.task import RapidStreamFuture, task

_logger = logging.getLogger(__name__)

RE_TASK_FAILED = """
==========================================
{task_name} failed:
================= STDERR =================
{stderr}
================= STDOUT =================
{stdout}
==========================================
"""

E_KILLING_PROCESS = "Killing the process {args} and its children..."
E_TIMEOUT = "The command {args} timed out after {timeout} seconds."
E_FAILED = "The command {args} failed with return code {returncode}."


def check_async_command(
    result: RapidStreamFuture[CompletedProcess[bytes]],
) -> None:
    """Check the result of a future of a command executed on the task cluster.

    Args:
        result (RapidStreamFuture[CompletedProcess[bytes]]): The future of the command
            to check.

    Raises:
        RuntimeError: If the command failed.
    """
    process = result.get()
    if process.returncode != 0:
        raise RuntimeError(
            RE_TASK_FAILED.format(
                task_name=result.task_name(),
                stderr=process.stderr,
                stdout=process.stdout,
            )
        )


def check_async_commands(
    results: list[RapidStreamFuture[CompletedProcess[bytes]]],
) -> None:
    """Check the results of a list of futures of commands executed on the task cluster.

    Args:
        results (list[RapidStreamFuture[CompletedProcess[bytes]]]): The futures of the
            commands to check.

    Raises:
        RuntimeError: If any of the commands failed.
    """
    for result in results:
        check_async_command(result)


def run_command_checked(
    args: list[str],
    cwd: str | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> None:
    """Run a command on the task cluster, and check the result.

    Args:
        args (list[str]): The arguments to the command.
        cwd (str | None): The working directory for the command to run in.
        as_bytes (int | None): The address space limit for the command to run with, in
            bytes.  If None, there will be no limit.
        timeout (int | None): The timeout in seconds for the command to finish.
            If None, this command may run indefinitely.

    Raises:
        RuntimeError: If the command failed.
    """
    result = run_command_async(args=args, cwd=cwd, as_bytes=as_bytes, timeout=timeout)
    check_async_command(result)


def run_command_async(
    args: list[str],
    cwd: str | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> RapidStreamFuture[CompletedProcess[bytes]]:
    """Run a command on a the task cluster.

    Args:
        args (list[str]): The arguments to the command.
        cwd (str | None): The working directory for the command to run in.
        as_bytes (int | None): The address space limit for the command to run with, in
            bytes.  If None, there will be no limit.
        timeout (int | None): The timeout in seconds for the command to finish.
            If None, this command may run indefinitely.

    Returns:
        RapidStreamFuture[CompletedProcess[bytes]]: Async result with type
            CompletedProcess[bytes] of the run.  The return value of the async result
            shall be checked to find out if the run was successful.
    """
    return run_command.submit(args, cwd, as_bytes, timeout)


@task
def run_command(
    args: list[str],
    cwd: str | None = None,
    as_bytes: int | None = None,
    timeout: int | None = None,
) -> CompletedProcess[bytes]:
    """Invoke a command with Popen and return the result.

    Args:
        args: The arguments to the command.
        cwd: The working directory for the command to run in.
        as_bytes: The address space limit for the command to run with, in bytes.
            If None, there will be no limit.
        timeout (int | None): The timeout in seconds for the command to finish.
            If None, this command may run indefinitely.

    Returns:
        CompletedProcess[bytes]: The result of the Vivado run.
    """

    def setlimits() -> None:
        """Set the address space limit for the command to run with, in bytes."""
        if as_bytes is None:
            return

        resource.setrlimit(
            resource.RLIMIT_AS,
            (as_bytes, as_bytes),
        )

    def tee(process: Popen[bytes], io: IO[bytes], lines: list[bytes]) -> None:
        """Read the output of the process and log it."""
        while process.poll() is None and (  # the process has not exited
            line := io.readline()
        ):  # and there is output to read
            _logger.debug("%s", line.decode().rstrip())
            lines.append(line)

    def kill_process_tree(process: Popen[bytes]) -> None:
        """Kill the process and its children."""
        psutil_process = Process(process.pid)
        for child in psutil_process.children(recursive=True):
            child.kill()
        psutil_process.kill()

    with tempfile.TemporaryDirectory() as temp_home_dir:
        # Set the HOME environment variable to a temporary directory to avoid
        # polluting the user's home directory with temporary files.  This is a
        # workaround for the fact that Vivado writes temporary files to $HOME.
        env = os.environ.copy()
        env["HOME"] = temp_home_dir

        stdout_lines: list[bytes] = []
        stderr_lines: list[bytes] = []

        with Popen(  # pylint: disable=subprocess-popen-preexec-fn
            args,
            cwd=cwd,
            stdout=PIPE,
            stderr=PIPE,
            preexec_fn=setlimits,
            env=env,
        ) as process:
            assert process.stdout
            assert process.stderr

            # Tee the output of the process to the logger
            threading.Thread(
                target=tee,
                args=(process, process.stdout, stdout_lines),
                daemon=True,
            ).start()

            # Tee the error output of the process to the logger
            threading.Thread(
                target=tee,
                args=(process, process.stderr, stderr_lines),
                daemon=True,
            ).start()

            def cleanup_process() -> None:
                """Kill the process and its children on timeout."""
                _logger.error(E_KILLING_PROCESS, args)
                kill_process_tree(process)

            atexit.register(cleanup_process)

            # Wait for the process to finish or kill it after the timeout
            try:
                process.wait(timeout=timeout)
            except TimeoutExpired:
                _logger.error(E_TIMEOUT, args, timeout)
                kill_process_tree(process)

            atexit.unregister(cleanup_process)

        if process.returncode != 0:
            _logger.error(E_FAILED, args, process.returncode)

        # Create a CompletedProcess object
        return CompletedProcess(
            process.args,
            process.returncode,
            b"".join(stdout_lines),
            b"".join(stderr_lines),
        )
