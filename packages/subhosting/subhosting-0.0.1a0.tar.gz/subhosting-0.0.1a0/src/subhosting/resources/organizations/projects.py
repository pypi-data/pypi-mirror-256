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
from ...types.shared import Project
from ...types.organizations import ProjectListResponse, project_list_params, project_create_params

__all__ = ["Projects", "AsyncProjects"]


class Projects(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProjectsWithRawResponse:
        return ProjectsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectsWithStreamingResponse:
        return ProjectsWithStreamingResponse(self)

    def create(
        self,
        organization_id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Project:
        """
        Create a project

        This API allows you to create a new project under the specified organization.
        The project name is optional; if not provided, a random name will be generated.

        Args:
          description: The description of the project. If this is `null`, an empty string will be set.

          name: The name of the project. This must be globally unique. If this is `null`, a
              random unique name will be generated.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return self._post(
            f"/organizations/{organization_id}/projects",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                project_create_params.ProjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Project,
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
    ) -> ProjectListResponse:
        """
        List projects of an organization

        This API returns a list of projects belonging to the specified organization in a
        pagenated manner. The URLs for the next, previous, first, and last page are
        returned in the `Link` header of the response, if any.

        Args:
          limit: The maximum number of items to return per page.

          order: Sort order, either `asc` or `desc`. Defaults to `asc`.

          page: The page number to return.

          q: Query by project name or project ID

          sort: The field to sort by, either `name` or `updated_at`. Defaults to `updated_at`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return self._get(
            f"/organizations/{organization_id}/projects",
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
                    project_list_params.ProjectListParams,
                ),
            ),
            cast_to=ProjectListResponse,
        )


class AsyncProjects(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProjectsWithRawResponse:
        return AsyncProjectsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectsWithStreamingResponse:
        return AsyncProjectsWithStreamingResponse(self)

    async def create(
        self,
        organization_id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Project:
        """
        Create a project

        This API allows you to create a new project under the specified organization.
        The project name is optional; if not provided, a random name will be generated.

        Args:
          description: The description of the project. If this is `null`, an empty string will be set.

          name: The name of the project. This must be globally unique. If this is `null`, a
              random unique name will be generated.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return await self._post(
            f"/organizations/{organization_id}/projects",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                project_create_params.ProjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Project,
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
    ) -> ProjectListResponse:
        """
        List projects of an organization

        This API returns a list of projects belonging to the specified organization in a
        pagenated manner. The URLs for the next, previous, first, and last page are
        returned in the `Link` header of the response, if any.

        Args:
          limit: The maximum number of items to return per page.

          order: Sort order, either `asc` or `desc`. Defaults to `asc`.

          page: The page number to return.

          q: Query by project name or project ID

          sort: The field to sort by, either `name` or `updated_at`. Defaults to `updated_at`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not organization_id:
            raise ValueError(f"Expected a non-empty value for `organization_id` but received {organization_id!r}")
        return await self._get(
            f"/organizations/{organization_id}/projects",
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
                    project_list_params.ProjectListParams,
                ),
            ),
            cast_to=ProjectListResponse,
        )


class ProjectsWithRawResponse:
    def __init__(self, projects: Projects) -> None:
        self._projects = projects

        self.create = to_raw_response_wrapper(
            projects.create,
        )
        self.list = to_raw_response_wrapper(
            projects.list,
        )


class AsyncProjectsWithRawResponse:
    def __init__(self, projects: AsyncProjects) -> None:
        self._projects = projects

        self.create = async_to_raw_response_wrapper(
            projects.create,
        )
        self.list = async_to_raw_response_wrapper(
            projects.list,
        )


class ProjectsWithStreamingResponse:
    def __init__(self, projects: Projects) -> None:
        self._projects = projects

        self.create = to_streamed_response_wrapper(
            projects.create,
        )
        self.list = to_streamed_response_wrapper(
            projects.list,
        )


class AsyncProjectsWithStreamingResponse:
    def __init__(self, projects: AsyncProjects) -> None:
        self._projects = projects

        self.create = async_to_streamed_response_wrapper(
            projects.create,
        )
        self.list = async_to_streamed_response_wrapper(
            projects.list,
        )
