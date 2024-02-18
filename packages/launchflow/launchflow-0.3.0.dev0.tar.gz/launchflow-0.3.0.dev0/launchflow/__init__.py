# ruff: noqa
from contextlib import contextmanager

from launchflow.resource import Resource

from . import gcp
from .flows.resource_flows import clean as _clean
from .flows.resource_flows import connect as _connect
from .flows.resource_flows import create as _create

# TODO: Add generic resource imports, like Postgres, StorageBucket, etc.
# This should probably live directly under launchflow, i.e. launchflow/postgres.py

_allow_connection_failures = False


def create(project: str, env: str, *resources: Resource):
    """Create resources in a project and environment.

    Args:
    - project (str): The name of the project.
    - env (str): The name of the environment.
    - resources (Resource): The resources to create.

    Example:
    ```python
    import launchflow as lf

    with lf.allow(connection_failures=True):
        bucket = lf.gcp.GCSBucket("bucket-for-lf")

    lf.create("project", "env", bucket)
    ```
    """
    _create(project, env, *resources)


def connect(project: str, env: str, *resources: Resource):
    """Connect resources in a project and environment. This will store connection info for the resources in the environment.

    Args:
    - project (str): The name of the project.
    - env (str): The name of the environment.
    - resources (Resource): The resources to connect.

    Example:
    ```python
    import launchflow as lf

    with lf.allow(connection_failures=True):
        bucket = lf.gcp.GCSBucket("bucket-for-lf")

    lf.connect("project", "env", bucket)
    ```
    """
    _connect(project, env, *resources)


def clean(project: str, env: str, *resources: Resource):
    """Clean resources in a project and environment. This will remove any resources that are part of the environment but not part of the resources list. This is the inverse of `create`.

    Args:
    - project (str): The name of the project.
    - env (str): The name of the environment.
    - resources (Resource): The resources to clean.

    Example:
    ```python
    import launchflow as lf

    with lf.allow(connection_failures=True):
        bucket = lf.gcp.GCSBucket("bucket-for-lf")

    lf.clean("project", "env", bucket)
    ```
    """
    _clean(project, env, *resources)


@contextmanager
def allow(*, connection_failures=False):
    """Context manager to allow connection failures during resource creation.

    Example:
    ```python
    import launchflow as lf

    with lf.allow(connection_failures=True):
        bucket = lf.gcp.GCSBucket("bucket-for-lf")

    lf.create("project", "env", bucket)
    ```
    """
    global _allow_connection_failures
    original_state = {"allow_connection_failures": _allow_connection_failures}
    try:
        _allow_connection_failures = connection_failures
        yield
    finally:
        _allow_connection_failures = original_state["allow_connection_failures"]
