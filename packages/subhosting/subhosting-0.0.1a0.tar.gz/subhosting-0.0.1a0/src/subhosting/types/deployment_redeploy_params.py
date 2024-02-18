# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["DeploymentRedeployParams"]


class DeploymentRedeployParams(TypedDict, total=False):
    databases: Optional[Dict[str, Optional[str]]]
    """KV database ID mappings to associate with the deployment.

    A key represents a KV database name (e.g. `"default"`), and a value is a KV
    database ID.

    Currently, only `"default"` database is supported. If any other database name is
    specified, that will be rejected.

    The provided KV database mappings will be _merged_ with the existing one, just
    like `env_vars`.

    If `databases` itself is not provided, no update will happen to the existing KV
    database mappings.
    """

    description: Optional[str]
    """A description of the created deployment.

    If not provided, no update will happen to the description.
    """

    env_vars: Optional[Dict[str, Optional[str]]]
    """
    A dictionary of environment variables to be set in the runtime environment of
    the deployment.

    The provided environment variables will be _merged_ with the existing one. For
    example, if the existing environment variables are:

    ```json
    {
    "a": "alice",
    "b": "bob"
    "c": "charlie"
    }
    ```

    and you pass the following environment variables in your redeploy request:

    ```json
    {
      "a": "alice2",
      "b": null,
      "d": "david"
    }
    ```

    then the result will be:

    ```json
    {
      "a": "alice2",
      "c": "charlie",
      "d": "david"
    }
    ```

    If `env_vars` itself is not provided, no update will happen to the existing
    environment variables.
    """
