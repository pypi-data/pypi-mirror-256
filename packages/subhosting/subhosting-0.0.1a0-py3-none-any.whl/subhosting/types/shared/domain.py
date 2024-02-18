# File generated from our OpenAPI spec by Stainless.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "Domain",
    "Certificate",
    "DNSRecord",
    "ProvisioningStatus",
    "ProvisioningStatusSuccess",
    "ProvisioningStatusFailed",
    "ProvisioningStatusPending",
    "ProvisioningStatusManual",
]


class Certificate(BaseModel):
    cipher: Literal["rsa", "ec"]

    created_at: datetime = FieldInfo(alias="createdAt")

    expires_at: datetime = FieldInfo(alias="expiresAt")

    updated_at: datetime = FieldInfo(alias="updatedAt")


class DNSRecord(BaseModel):
    content: str

    name: str

    type: str


class ProvisioningStatusSuccess(BaseModel):
    code: Literal["success"]


class ProvisioningStatusFailed(BaseModel):
    code: Literal["failed"]

    message: str


class ProvisioningStatusPending(BaseModel):
    code: Literal["pending"]


class ProvisioningStatusManual(BaseModel):
    code: Literal["manual"]


ProvisioningStatus = Union[
    ProvisioningStatusSuccess, ProvisioningStatusFailed, ProvisioningStatusPending, ProvisioningStatusManual
]


class Domain(BaseModel):
    id: str
    """The ID of the domain."""

    token: str

    certificates: List[Certificate]
    """TLS certificates for the domain."""

    created_at: datetime = FieldInfo(alias="createdAt")

    dns_records: List[DNSRecord] = FieldInfo(alias="dnsRecords")
    """These records are used to verify the ownership of the domain."""

    domain: str
    """The domain value."""

    is_validated: bool = FieldInfo(alias="isValidated")
    """Whether the domain's ownership is validated or not."""

    organization_id: str = FieldInfo(alias="organizationId")
    """The ID of the organization that the domain is associated with."""

    provisioning_status: ProvisioningStatus = FieldInfo(alias="provisioningStatus")

    updated_at: datetime = FieldInfo(alias="updatedAt")

    deployment_id: Optional[str] = FieldInfo(alias="deploymentId", default=None)
    """A deployment ID

    Note that this is not UUID v4, as opposed to organization ID and project ID.
    """

    project_id: Optional[str] = FieldInfo(alias="projectId", default=None)
    """The ID of the project that the domain is associated with.

    If the domain is not associated with any project, this field is omitted.
    """
