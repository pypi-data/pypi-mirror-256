# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["AnalyticsGetParams"]


class AnalyticsGetParams(TypedDict, total=False):
    since: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """Start of the time range in RFC3339 format.

    Defaults to 24 hours ago.
    """

    until: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """End of the time range in RFC3339 format.

    Defaults to the current time.
    """
