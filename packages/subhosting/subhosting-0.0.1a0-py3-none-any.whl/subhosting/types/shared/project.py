# File generated from our OpenAPI spec by Stainless.

from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Project"]


class Project(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    description: str

    name: str

    updated_at: datetime = FieldInfo(alias="updatedAt")
