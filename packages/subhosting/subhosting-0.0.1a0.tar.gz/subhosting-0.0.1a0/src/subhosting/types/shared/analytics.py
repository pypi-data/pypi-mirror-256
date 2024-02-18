# File generated from our OpenAPI spec by Stainless.

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["Analytics", "Field"]


class Field(BaseModel):
    name: str

    type: Literal["time", "number", "string", "boolean", "other"]
    """A data type that analytic data can be represented in.

    Inspired by Grafana's data types defined at:
    https://github.com/grafana/grafana/blob/e3288834b37b9aac10c1f43f0e621b35874c1f8a/packages/grafana-data/src/types/dataFrame.ts#L11-L23
    """


class Analytics(BaseModel):
    fields: List[Field]

    values: List[List[Union[datetime, float, str, bool, object]]]
