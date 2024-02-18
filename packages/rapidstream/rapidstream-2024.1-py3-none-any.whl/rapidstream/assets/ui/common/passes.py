"""Generic type for transformation passes of RapidStream."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

from collections.abc import Callable
from pathlib import Path
from typing import Concatenate, ParamSpec

_P = ParamSpec("_P")


class Pass:
    """A pass for RapidStream."""

    def __init__(
        self,
        name: str,
        func: Callable[Concatenate[Path, Path, Path, _P], None],
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> None:
        """Initialize the Pass class.

        Args:
            name: The name of the pass.
            func: The function to run for the pass.  The function takes the following
                arguments:
                (1) input_json_path: The path to the input JSON file.
                (2) output_json_path: The path to the output JSON file.
                (3) log_path: The path to the log file.
                (4) *args: The additional arguments for the pass.
                (5) **kwargs: The additional keyword arguments for the pass.
            args: The additional arguments for the pass.
            kwargs: The additional keyword arguments for the pass.
        """
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(
        self,
        input_json_path: Path,
        output_json_path: Path,
        log_path: Path,
    ) -> None:
        """Call the pass function."""
        self.func(
            input_json_path,
            output_json_path,
            log_path,
            *self.args,
            **self.kwargs,
        )
