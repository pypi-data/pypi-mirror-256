"""The RapidStream's Dask wrapper for submitting tasks and obtaining future results.

A future is a handle to the result of an asynchronous computation.  It is a placeholder
for the result of a computation that does not yet exist.  The future can be used to
retrieve the result of the computation when it is available.

This module provides a wrapper over Dask's future and task to run tasks in parallel on
the Dask cluster.  The task is a wrapper over Dask's client.submit that runs a RapidStream
task.  The future is a Dask future of a RapidStream task's result.

The main purpose of this module is to provide a simple abstraction for easier framework
switching.  It further provides a typing hint for the type of the task.
"""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import logging
from collections.abc import Callable
from typing import Generic, TypeVar

from dask.distributed import Future

from rapidstream.assets.cluster.client import DaskClient

_X = TypeVar("_X")

_logger = logging.getLogger(__name__)

D_GETTING_RESULT = 'Getting the result of the future of task "%s"...'
D_GETTING_TIMEOUT = 'Getting the result of the future of task "%s" with timeout %s...'
D_TASK_FINISHED = 'Task "%s" finished.'
D_RUNNING_TASK_ASYNCHRONOUSLY = 'Running task "%s" asynchronously: %s %s...'


class RapidStreamFuture(Generic[_X]):
    """A Dask future of a RapidStream task.

    Attributes:
        _future (Future): The future of the task's result.
        _func_name (str): The name of the function generating the future.
        _args (object): The arguments of the function generating the future.
        _kwds (object): The keyword arguments of the function generating the future.
    """

    _future: Future
    _func_name: str
    _args: object
    _kwds: object

    def __init__(
        self,
        future: Future,
        func_name: str,
        *args: object,
        **kwds: object,
    ) -> None:
        """Initialize the future.

        Args:
            future (Future): The Dask future of the task's result.
            func_name (str): The name of the function generating the future.
            args (object): The arguments of the function generating the future.
            kwds (object): The keyword arguments of the function generating the future.
        """
        self._future = future
        self._func_name = func_name
        self._args = args
        self._kwds = kwds

    def get(self, timeout: int | None = None) -> _X:
        """Wait and get the value of the future.

        Args:
            timeout (int | None): The timeout in seconds to wait for the future.

        Returns:
            _X: The result of the job.
        """
        if timeout is None:
            _logger.debug(D_GETTING_RESULT, self.task_name())
        else:
            _logger.debug(D_GETTING_TIMEOUT, self.task_name(), timeout)

        result: _X = self._future.result(timeout=timeout)  # type: ignore

        _logger.debug(D_TASK_FINISHED, self.task_name())
        return result

    def task_name(self) -> str:
        """Return the name of the task."""
        return f"{self._func_name}({self._args}, {self._kwds})"


class RapidStreamTask(Generic[_X]):
    """A wrapper over Dask client.submit that runs a RapidStream task.

    Attributes:
        func (Callable[..., _X]): The function to run.
        opts (object): The options to pass to the task function.
    """

    def __init__(self, func: Callable[..., _X]) -> None:
        """Initialize the task.

        Args:
            func (Callable[..., _X]): The function to run as a task.
        """
        self.func = func

    def __call__(self, *args: object, **kwds: object) -> _X:
        """Run the task synchronously."""
        return self.func(*args, **kwds)

    def submit(self, *args: object, **kwds: object) -> RapidStreamFuture[_X]:
        """Run the task asynchronously."""
        _logger.debug(D_RUNNING_TASK_ASYNCHRONOUSLY, self.func.__name__, args, kwds)
        return RapidStreamFuture(
            DaskClient.get().client.submit(self.func, *args, pure=False, **kwds),  # type: ignore
            self.func.__name__,
            *args,
            **kwds,
        )


def task(func: Callable[..., _X]) -> RapidStreamTask[_X]:
    """Decorator to define a task to be executed on the Dask cluster."""
    return RapidStreamTask(func)
