# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ProjectUpdateParams"]


class ProjectUpdateParams(TypedDict, total=False):
    description: Optional[str]
    """The description of the project to be updated to.

    If this is `null`, no update will be made to the project description.
    """

    name: Optional[str]
    """The name of the project to be updated to.

    This must be globally unique. If this is `null`, no update will be made to the
    project name.
    """
