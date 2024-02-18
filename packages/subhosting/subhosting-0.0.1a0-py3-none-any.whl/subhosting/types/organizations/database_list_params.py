# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["DatabaseListParams"]


class DatabaseListParams(TypedDict, total=False):
    limit: Optional[int]
    """The maximum number of items to return per page."""

    order: Optional[str]
    """Sort order, either `asc` or `desc`. Defaults to `asc`."""

    page: Optional[int]
    """The page number to return."""

    q: Optional[str]
    """Query by KV database ID"""

    sort: Optional[str]
    """The field to sort by. Currently only `created_at` is supported."""
