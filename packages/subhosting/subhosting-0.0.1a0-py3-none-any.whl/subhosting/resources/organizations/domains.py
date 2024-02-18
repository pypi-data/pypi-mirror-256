# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import (
    make_request_options,
)
from ...types.shared import Domain
from ...types.organizations import DomainListResponse, domain_list_params, domain_create_params

__all__ = ["Domains", "AsyncDomains"]


class Domains(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DomainsWithRawResponse:
        return DomainsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DomainsWithStreamingResponse:
        return DomainsWithStreamingResponse(self)

    def create(
        self,
        organization_id: str,
        *,
        domain: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Domain:
        """
        Add a domain to an organization

        This API allows you to add a new domain to the specified organization.

        Before use, added domain needs to be verified, and also TLS certificates for the
        domain need to be provisioned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return self._post(
            f"/organizations/{organization_id}/domains",
            body=maybe_transform({"domain": domain}, domain_create_params.DomainCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Domain,
        )

    def list(
        self,
        organization_id: str,
        *,
        limit: Optional[int] | NotGiven = NOT_GIVEN,
        order: Optional[str] | NotGiven = NOT_GIVEN,
        page: Optional[int] | NotGiven = NOT_GIVEN,
        q: Optional[str] | NotGiven = NOT_GIVEN,
        sort: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DomainListResponse:
        """
        List domains of an organization

        This API returns a list of domains belonging to the specified organization in a
        pagenated manner.

        The URLs for the next, previous, first, and last page are returned in the `Link`
        header of the response, if any.

        Args:
          limit: The maximum number of items to return per page.

          order: Sort order, either `asc` or `desc`. Defaults to `asc`.

          page: The page number to return.

          q: Query by domain

          sort: The field to sort by, `domain`, `created_at`, or `updated_at`. Defaults to
              `updated_at`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return self._get(
            f"/organizations/{organization_id}/domains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "order": order,
                        "page": page,
                        "q": q,
                        "sort": sort,
                    },
                    domain_list_params.DomainListParams,
                ),
            ),
            cast_to=DomainListResponse,
        )


class AsyncDomains(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDomainsWithRawResponse:
        return AsyncDomainsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDomainsWithStreamingResponse:
        return AsyncDomainsWithStreamingResponse(self)

    async def create(
        self,
        organization_id: str,
        *,
        domain: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Domain:
        """
        Add a domain to an organization

        This API allows you to add a new domain to the specified organization.

        Before use, added domain needs to be verified, and also TLS certificates for the
        domain need to be provisioned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return await self._post(
            f"/organizations/{organization_id}/domains",
            body=maybe_transform({"domain": domain}, domain_create_params.DomainCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Domain,
        )

    async def list(
        self,
        organization_id: str,
        *,
        limit: Optional[int] | NotGiven = NOT_GIVEN,
        order: Optional[str] | NotGiven = NOT_GIVEN,
        page: Optional[int] | NotGiven = NOT_GIVEN,
        q: Optional[str] | NotGiven = NOT_GIVEN,
        sort: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DomainListResponse:
        """
        List domains of an organization

        This API returns a list of domains belonging to the specified organization in a
        pagenated manner.

        The URLs for the next, previous, first, and last page are returned in the `Link`
        header of the response, if any.

        Args:
          limit: The maximum number of items to return per page.

          order: Sort order, either `asc` or `desc`. Defaults to `asc`.

          page: The page number to return.

          q: Query by domain

          sort: The field to sort by, `domain`, `created_at`, or `updated_at`. Defaults to
              `updated_at`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return await self._get(
            f"/organizations/{organization_id}/domains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "order": order,
                        "page": page,
                        "q": q,
                        "sort": sort,
                    },
                    domain_list_params.DomainListParams,
                ),
            ),
            cast_to=DomainListResponse,
        )


class DomainsWithRawResponse:
    def __init__(self, domains: Domains) -> None:
        self._domains = domains

        self.create = to_raw_response_wrapper(
            domains.create,
        )
        self.list = to_raw_response_wrapper(
            domains.list,
        )


class AsyncDomainsWithRawResponse:
    def __init__(self, domains: AsyncDomains) -> None:
        self._domains = domains

        self.create = async_to_raw_response_wrapper(
            domains.create,
        )
        self.list = async_to_raw_response_wrapper(
            domains.list,
        )


class DomainsWithStreamingResponse:
    def __init__(self, domains: Domains) -> None:
        self._domains = domains

        self.create = to_streamed_response_wrapper(
            domains.create,
        )
        self.list = to_streamed_response_wrapper(
            domains.list,
        )


class AsyncDomainsWithStreamingResponse:
    def __init__(self, domains: AsyncDomains) -> None:
        self._domains = domains

        self.create = async_to_streamed_response_wrapper(
            domains.create,
        )
        self.list = async_to_streamed_response_wrapper(
            domains.list,
        )
