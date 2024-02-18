# File generated from our OpenAPI spec by Stainless.

from typing import List
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["AppLogGetResponse", "AppLogGetResponseItem"]


class AppLogGetResponseItem(BaseModel):
    level: Literal["error", "warning", "info", "debug"]

    message: str

    region: Literal[
        "gcp-asia-east1",
        "gcp-asia-east2",
        "gcp-asia-northeast1",
        "gcp-asia-northeast2",
        "gcp-asia-northeast3",
        "gcp-asia-south1",
        "gcp-asia-south2",
        "gcp-asia-southeast1",
        "gcp-asia-southeast2",
        "gcp-australia-southeast1",
        "gcp-australia-southeast2",
        "gcp-europe-central2",
        "gcp-europe-north1",
        "gcp-europe-southwest1",
        "gcp-europe-west1",
        "gcp-europe-west2",
        "gcp-europe-west3",
        "gcp-europe-west4",
        "gcp-europe-west6",
        "gcp-europe-west8",
        "gcp-me-west1",
        "gcp-northamerica-northeast1",
        "gcp-northamerica-northeast2",
        "gcp-southamerica-east1",
        "gcp-southamerica-west1",
        "gcp-us-central1",
        "gcp-us-east1",
        "gcp-us-east4",
        "gcp-us-east5",
        "gcp-us-south1",
        "gcp-us-west1",
        "gcp-us-west2",
        "gcp-us-west3",
        "gcp-us-west4",
    ]

    time: datetime
    """Log timestamp"""


AppLogGetResponse = List[AppLogGetResponseItem]
