# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["AppLogGetParams"]


class AppLogGetParams(TypedDict, total=False):
    cursor: Optional[str]
    """
    Opaque value that represents the cursor of the last log returned in the previous
    request.

    This is only effective for the past log mode.
    """

    level: Literal["error", "warning", "info", "debug"]
    """Log level(s) to filter logs by.

    Defaults to all levels (i.e. no filter applied).

    Multiple levels can be specified using comma-separated format.
    """

    limit: Optional[int]
    """Maximum number of logs to return in one request.

    This is only effective for the past log mode.
    """

    order: Optional[str]
    """Sort order, either `asc` or `desc`. Defaults to `desc`.

    For backward compatibility, `timeAsc` and `timeDesc` are also supported, but
    deprecated.

    This is only effective for the past log mode.
    """

    q: Optional[str]
    """Text to search for in log message."""

    region: Literal[
        "gcp-asia-east1",
        "gcp-asia-east2",
        "gcp-asia-northeast1",
        "gcp-asia-northeast2",
        "gcp-asia-northeast3",
        "gcp-asia-south1",
        "gcp-asia-south2",
        "gcp-asia-southeast1",
        "gcp-asia-southeast2",
        "gcp-australia-southeast1",
        "gcp-australia-southeast2",
        "gcp-europe-central2",
        "gcp-europe-north1",
        "gcp-europe-southwest1",
        "gcp-europe-west1",
        "gcp-europe-west2",
        "gcp-europe-west3",
        "gcp-europe-west4",
        "gcp-europe-west6",
        "gcp-europe-west8",
        "gcp-me-west1",
        "gcp-northamerica-northeast1",
        "gcp-northamerica-northeast2",
        "gcp-southamerica-east1",
        "gcp-southamerica-west1",
        "gcp-us-central1",
        "gcp-us-east1",
        "gcp-us-east4",
        "gcp-us-east5",
        "gcp-us-south1",
        "gcp-us-west1",
        "gcp-us-west2",
        "gcp-us-west3",
        "gcp-us-west4",
    ]
    """Region(s) to filter logs by.

    Defaults to all regions (i.e. no filter applied).

    Multiple regions can be specified using comma-separated format.
    """

    since: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Start time of the time range to filter logs by.

    Defaults to the Unix Epoch (though the log retention period is 2 weeks as of
    now).

    If neither `since` nor `until` is specified, real-time logs are returned.
    """

    sort: Optional[str]
    """The field to sort by. Currently only `time` is supported.

    This is only effective for the past log mode.
    """

    until: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """End time of the time range to filter logs by.

    Defaults to the current time.

    If neither `since` nor `until` is specified, real-time logs are returned.
    """
