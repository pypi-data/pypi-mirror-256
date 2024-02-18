"""Client of Dask cluster for RapidStream to run multiple tasks in parallel.

This module wraps the Dask cluster and client to provide a global job queue for
RapidStream to run tasks in parallel.

Dask is a flexible parallel computing library, which supports a diverse set of
parallel computing backends.  By default, the local cluster is used, which runs the
tasks in parallel with multiprocessing on the local machine.  When the address
of a remote Dask cluster is specified, the tasks will be distributed to the cluster.

Please refer to RapidStream's documentation for more details about the Dask client and
how to setup a remote Dask cluster for higher scalability.
"""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""
