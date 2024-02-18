# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["CertificateCreateParams"]


class CertificateCreateParams(TypedDict, total=False):
    certificate_chain: Required[Annotated[str, PropertyInfo(alias="certificateChain")]]
    """The PRM encoded certificate chain for the TLS certificate"""

    private_key: Required[Annotated[str, PropertyInfo(alias="privateKey")]]
    """The PEM encoded private key for the TLS certificate"""
