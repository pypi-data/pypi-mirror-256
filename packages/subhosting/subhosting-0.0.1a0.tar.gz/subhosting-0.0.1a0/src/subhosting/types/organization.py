# File generated from our OpenAPI spec by Stainless.

from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Organization"]


class Organization(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    name: str

    updated_at: datetime = FieldInfo(alias="updatedAt")
