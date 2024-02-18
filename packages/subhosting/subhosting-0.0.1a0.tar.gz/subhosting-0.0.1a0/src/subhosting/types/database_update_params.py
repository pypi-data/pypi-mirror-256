# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["DatabaseUpdateParams"]


class DatabaseUpdateParams(TypedDict, total=False):
    description: Optional[str]
    """The description of the KV database to be updated to.

    If this is `null`, no update will be made to the KV database description.
    """
