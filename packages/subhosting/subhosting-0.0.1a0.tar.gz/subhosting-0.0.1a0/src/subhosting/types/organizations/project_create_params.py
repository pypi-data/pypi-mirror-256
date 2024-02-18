# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ProjectCreateParams"]


class ProjectCreateParams(TypedDict, total=False):
    description: Optional[str]
    """The description of the project. If this is `null`, an empty string will be set."""

    name: Optional[str]
    """The name of the project.

    This must be globally unique. If this is `null`, a random unique name will be
    generated.
    """
