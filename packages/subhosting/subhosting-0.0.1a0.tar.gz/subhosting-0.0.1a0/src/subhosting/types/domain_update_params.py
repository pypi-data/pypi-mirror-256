# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DomainUpdateParams"]


class DomainUpdateParams(TypedDict, total=False):
    deployment_id: Annotated[str, PropertyInfo(alias="deploymentId")]
    """A deployment ID

    Note that this is not UUID v4, as opposed to organization ID and project ID.
    """
