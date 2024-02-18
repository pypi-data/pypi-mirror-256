# File generated from our OpenAPI spec by Stainless.

from typing import List

from ..._models import BaseModel

__all__ = ["BuildLogGetResponse", "BuildLogGetResponseItem"]


class BuildLogGetResponseItem(BaseModel):
    level: str

    message: str


BuildLogGetResponse = List[BuildLogGetResponseItem]
