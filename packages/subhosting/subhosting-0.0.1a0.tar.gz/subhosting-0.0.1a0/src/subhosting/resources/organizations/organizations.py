# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from ...types import Organization
from .domains import (
    Domains,
    AsyncDomains,
    DomainsWithRawResponse,
    AsyncDomainsWithRawResponse,
    DomainsWithStreamingResponse,
    AsyncDomainsWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .projects import (
    Projects,
    AsyncProjects,
    ProjectsWithRawResponse,
    AsyncProjectsWithRawResponse,
    ProjectsWithStreamingResponse,
    AsyncProjectsWithStreamingResponse,
)
from ..._compat import cached_property
from .analytics import (
    Analytics,
    AsyncAnalytics,
    AnalyticsWithRawResponse,
    AsyncAnalyticsWithRawResponse,
    AnalyticsWithStreamingResponse,
    AsyncAnalyticsWithStreamingResponse,
)
from .databases import (
    Databases,
    AsyncDatabases,
    DatabasesWithRawResponse,
    AsyncDatabasesWithRawResponse,
    DatabasesWithStreamingResponse,
    AsyncDatabasesWithStreamingResponse,
)
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

__all__ = ["Organizations", "AsyncOrganizations"]


class Organizations(SyncAPIResource):
    @cached_property
    def analytics(self) -> Analytics:
        return Analytics(self._client)

    @cached_property
    def projects(self) -> Projects:
        return Projects(self._client)

    @cached_property
    def databases(self) -> Databases:
        return Databases(self._client)

    @cached_property
    def domains(self) -> Domains:
        return Domains(self._client)

    @cached_property
    def with_raw_response(self) -> OrganizationsWithRawResponse:
        return OrganizationsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrganizationsWithStreamingResponse:
        return OrganizationsWithStreamingResponse(self)

    def get(
        self,
        organization_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Organization:
        """
        Get organization details

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return self._get(
            f"/organizations/{organization_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Organization,
        )


class AsyncOrganizations(AsyncAPIResource):
    @cached_property
    def analytics(self) -> AsyncAnalytics:
        return AsyncAnalytics(self._client)

    @cached_property
    def projects(self) -> AsyncProjects:
        return AsyncProjects(self._client)

    @cached_property
    def databases(self) -> AsyncDatabases:
        return AsyncDatabases(self._client)

    @cached_property
    def domains(self) -> AsyncDomains:
        return AsyncDomains(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncOrganizationsWithRawResponse:
        return AsyncOrganizationsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrganizationsWithStreamingResponse:
        return AsyncOrganizationsWithStreamingResponse(self)

    async def get(
        self,
        organization_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Organization:
        """
        Get organization details

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return await self._get(
            f"/organizations/{organization_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Organization,
        )


class OrganizationsWithRawResponse:
    def __init__(self, organizations: Organizations) -> None:
        self._organizations = organizations

        self.get = to_raw_response_wrapper(
            organizations.get,
        )

    @cached_property
    def analytics(self) -> AnalyticsWithRawResponse:
        return AnalyticsWithRawResponse(self._organizations.analytics)

    @cached_property
    def projects(self) -> ProjectsWithRawResponse:
        return ProjectsWithRawResponse(self._organizations.projects)

    @cached_property
    def databases(self) -> DatabasesWithRawResponse:
        return DatabasesWithRawResponse(self._organizations.databases)

    @cached_property
    def domains(self) -> DomainsWithRawResponse:
        return DomainsWithRawResponse(self._organizations.domains)


class AsyncOrganizationsWithRawResponse:
    def __init__(self, organizations: AsyncOrganizations) -> None:
        self._organizations = organizations

        self.get = async_to_raw_response_wrapper(
            organizations.get,
        )

    @cached_property
    def analytics(self) -> AsyncAnalyticsWithRawResponse:
        return AsyncAnalyticsWithRawResponse(self._organizations.analytics)

    @cached_property
    def projects(self) -> AsyncProjectsWithRawResponse:
        return AsyncProjectsWithRawResponse(self._organizations.projects)

    @cached_property
    def databases(self) -> AsyncDatabasesWithRawResponse:
        return AsyncDatabasesWithRawResponse(self._organizations.databases)

    @cached_property
    def domains(self) -> AsyncDomainsWithRawResponse:
        return AsyncDomainsWithRawResponse(self._organizations.domains)


class OrganizationsWithStreamingResponse:
    def __init__(self, organizations: Organizations) -> None:
        self._organizations = organizations

        self.get = to_streamed_response_wrapper(
            organizations.get,
        )

    @cached_property
    def analytics(self) -> AnalyticsWithStreamingResponse:
        return AnalyticsWithStreamingResponse(self._organizations.analytics)

    @cached_property
    def projects(self) -> ProjectsWithStreamingResponse:
        return ProjectsWithStreamingResponse(self._organizations.projects)

    @cached_property
    def databases(self) -> DatabasesWithStreamingResponse:
        return DatabasesWithStreamingResponse(self._organizations.databases)

    @cached_property
    def domains(self) -> DomainsWithStreamingResponse:
        return DomainsWithStreamingResponse(self._organizations.domains)


class AsyncOrganizationsWithStreamingResponse:
    def __init__(self, organizations: AsyncOrganizations) -> None:
        self._organizations = organizations

        self.get = async_to_streamed_response_wrapper(
            organizations.get,
        )

    @cached_property
    def analytics(self) -> AsyncAnalyticsWithStreamingResponse:
        return AsyncAnalyticsWithStreamingResponse(self._organizations.analytics)

    @cached_property
    def projects(self) -> AsyncProjectsWithStreamingResponse:
        return AsyncProjectsWithStreamingResponse(self._organizations.projects)

    @cached_property
    def databases(self) -> AsyncDatabasesWithStreamingResponse:
        return AsyncDatabasesWithStreamingResponse(self._organizations.databases)

    @cached_property
    def domains(self) -> AsyncDomainsWithStreamingResponse:
        return AsyncDomainsWithStreamingResponse(self._organizations.domains)
