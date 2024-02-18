# File generated from our OpenAPI spec by Stainless.

from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["KvDatabase"]


class KvDatabase(BaseModel):
    id: str
    """A KV database ID"""

    created_at: datetime = FieldInfo(alias="createdAt")

    description: str
    """A description of this KV database"""

    organization_id: str = FieldInfo(alias="organizationId")
    """An organization ID that this KV database belongs to"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
