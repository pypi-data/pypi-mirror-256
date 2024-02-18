# File generated from our OpenAPI spec by Stainless.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Deployment"]


class Deployment(BaseModel):
    id: str
    """A deployment ID

    Note that this is not UUID v4, as opposed to organization ID and project ID.
    """

    created_at: datetime = FieldInfo(alias="createdAt")

    databases: Dict[str, str]
    """
    The KV databases that this deployment has access to. Currently, only `"default"`
    database is supported.
    """

    project_id: str = FieldInfo(alias="projectId")

    status: Literal["failed", "pending", "success"]
    """The status of a deployment."""

    updated_at: datetime = FieldInfo(alias="updatedAt")

    description: Optional[str] = None
    """The description of this deployment.

    This is present only when the `status` is `success`.
    """

    domains: Optional[List[str]] = None
