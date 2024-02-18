"""Singleton implementation."""

from __future__ import annotations

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import logging
from typing import Generic, TypeVar

_X = TypeVar("_X")

_logger = logging.getLogger(__name__)


W_INITIALIZED = (
    "Singleton class has already been initialized but the initializer has been called"
    " again.  This may happen when a singleton class is initialized in a test and the"
    " tests reuse the same singleton inside a process.  This initialization call is"
    " thus ignored.  If this is not the case, a bug may exist."
)

RE_NOT_INITIALIZED = (
    "Singleton class has not been initialized.  A singleton object must be initialized"
    " using Class() before it can be obtained with Class.get()."
)


class Singleton(type, Generic[_X]):
    """Singleton metaclass.

    To create a singleton class, use class `Class(metaclass=Singleton["Class"])`.  mypy
    will complain about the type of the metaclass, but it is correct.  A `mypy: ignore`
    annotation can be added to the class to suppress the error.

    To initialize a singleton class, use `Class(*args, **kwargs)`.  To get the singleton
    instance, use `Class.get()`.
    """

    _instances: dict[Singleton[_X], _X] = {}

    def __call__(cls, *args: object, **kwargs: object) -> _X:
        """Initialize the instance of the singleton class."""
        if cls in cls._instances:
            _logger.error(W_INITIALIZED)
        else:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

    def get(cls) -> _X:
        """Get the instance of the singleton class.

        Returns:
            The instance of the singleton class.

        Raises:
            RuntimeError: If the singleton class has not been initialized.  A singleton
                object must be initialized using Class() before it can be obtained with
                Class.get().
        """
        if cls not in cls._instances:
            raise RuntimeError(RE_NOT_INITIALIZED)

        return cls._instances[cls]
