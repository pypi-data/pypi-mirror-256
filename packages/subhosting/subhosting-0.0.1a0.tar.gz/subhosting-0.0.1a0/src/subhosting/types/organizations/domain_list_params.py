# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["DomainListParams"]


class DomainListParams(TypedDict, total=False):
    limit: Optional[int]
    """The maximum number of items to return per page."""

    order: Optional[str]
    """Sort order, either `asc` or `desc`. Defaults to `asc`."""

    page: Optional[int]
    """The page number to return."""

    q: Optional[str]
    """Query by domain"""

    sort: Optional[str]
    """The field to sort by, `domain`, `created_at`, or `updated_at`.

    Defaults to `updated_at`.
    """
