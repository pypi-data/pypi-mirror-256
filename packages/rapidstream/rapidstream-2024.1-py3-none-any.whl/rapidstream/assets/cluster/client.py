"""The RapidStream's Dask client wrapper to run multiple tasks in parallel."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import logging

import psutil
from dask.distributed import Client, LocalCluster

from rapidstream.assets.utilities.singleton import (  # pylint: disable=unused-import
    Singleton,
)

_logger = logging.getLogger(__name__)

VE_BOTH_GIVEN = "Only one of the address and jobs can be specified, but both are given."
VE_NON_POSITIVE_JOBS = "The number of jobs must be positive, but {jobs} is given."

RE_NO_LOCAL_CLUSTER = (
    "The local cluster is not started as the address is specified."
    "  Unable to manage the cluster from the local cluster property."
)

I_ADDRESS = "The Dask cluster is set to be at %s."
I_JOBS = "RapidStream will run with %s parallel jobs."
I_STARTING_LOCAL_CLUSTER = "Starting the local Dask cluster..."
I_CONNECTING_REMOTE_CLUSTER = "Connecting to the remote Dask cluster at %s..."


class DaskClient(metaclass=Singleton["DaskClient"]):  # type: ignore
    """A singleton class that specifies the global Dask client.

    To set the global Dask cluster of the client, call `DaskClient(...)`. Afterward, use
    `DaskClient.get().client` to access the client of the global Dask cluster.

    If the address of the Dask cluster is not specified, the local cluster will be
    started with the number of parallel jobs specified by `jobs`.  If the address
    is specified, the client will connect to the remote cluster.

    This class is automatically used by
    `rapidstream.assets.cluster.task.RapidStreamTask`, and before any usage of
    `RapidStreamTask.task`, the global client must be initialized by `DaskClient()`.

    Attributes:
        _client (Client | None): The Dask client of the cluster.
        _local_cluster (LocalCluster | None): The local cluster instance, if started.
        _address (str | None): The address of the Dask cluster to connect to.
        _jobs (int | None): The number of parallel jobs of the local cluster.
        _quiet (bool): If True, the logs of the Dask cluster will be suppressed.
    """

    _client: Client | None = None
    _local_cluster: LocalCluster | None = None

    _address: str | None = None
    _jobs: int | None = None
    _quiet: bool = True

    def __init__(
        self,
        *,
        address: str | None = None,
        jobs: int | None = None,
        quiet: bool = True,
    ) -> None:
        """Configure the Dask cluster and its client.

        The object will be initialized lazily when it is first accessed by the
        `client` property or the `local_cluster` property.  This is for performance
        reasons, as the Dask cluster and its client are not always needed.

        Args:
            address (str | None): The address of the Dask cluster to connect to.  If not
                specified, a cluster will be started locally.
            jobs (int | None): The number of parallel jobs of the local cluster.  If not
                specified, the number of parallel jobs will be set to the currently
                available memory size divided by 8 GB.  This option is only effective
                when the address is not specified.  Otherwise, no local cluster will be
                started.
            quiet (bool): If True, the logs of the Dask cluster will be suppressed.
        """
        self._address = address
        self._jobs = jobs
        self._quiet = quiet

        if self._address is not None and self._jobs is not None:
            raise ValueError(VE_BOTH_GIVEN)

        if self._jobs is not None and self._jobs <= 0:
            raise ValueError(VE_NON_POSITIVE_JOBS.format(jobs=self._jobs))

        if self._address is not None:
            _logger.info(I_ADDRESS, self._address)
        else:
            if self._jobs is None:
                # The available memory / 8 GB for the job count as a default.
                self._jobs = psutil.virtual_memory().available // (
                    8 * 1024 * 1024 * 1024
                )
            _logger.info(I_JOBS, self._jobs)

    @property
    def client(self) -> Client:
        """The Dask client of the cluster."""
        self.ensure_ready()
        assert self._client is not None, "The client failed to initialize."
        return self._client

    @property
    def local_cluster(self) -> LocalCluster:
        """The local cluster instance, if started."""
        self.ensure_ready()
        if self._local_cluster is None:
            raise RuntimeError(RE_NO_LOCAL_CLUSTER)
        return self._local_cluster

    def ensure_ready(self) -> None:
        """Ensure that the Dask client is ready.

        If the client has not been initialized, this method will start the local cluster
        or connect to the remote cluster, depending on the address specified.
        """
        # If the client is already initialized, return.
        if self._client is not None:
            return

        if self._address is None:
            # Create a local Dask cluster if the address is not specified.
            _logger.info(I_STARTING_LOCAL_CLUSTER)

            self._local_cluster = LocalCluster(  # type: ignore
                n_workers=self._jobs,
                memory_limit=0,
                processes=True,
                threads_per_worker=1,
                scheduler_port=0,
                silence_logs=False if not self._quiet else logging.CRITICAL,
                dashboard_address=":0",
            )
            self._client = Client(self._local_cluster)  # type: ignore

        else:
            # Otherwise, connect to the specified Dask cluster.
            _logger.info(I_CONNECTING_REMOTE_CLUSTER, self._address)

            self._client = Client(self._address)  # type: ignore
