# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional

import httpx

from ...types import project_update_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import maybe_transform
from ..._compat import cached_property
from .analytics import (
    Analytics,
    AsyncAnalytics,
    AnalyticsWithRawResponse,
    AsyncAnalyticsWithRawResponse,
    AnalyticsWithStreamingResponse,
    AsyncAnalyticsWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .deployments import (
    Deployments,
    AsyncDeployments,
    DeploymentsWithRawResponse,
    AsyncDeploymentsWithRawResponse,
    DeploymentsWithStreamingResponse,
    AsyncDeploymentsWithStreamingResponse,
)
from ..._base_client import (
    make_request_options,
)
from ...types.shared import Project

__all__ = ["Projects", "AsyncProjects"]


class Projects(SyncAPIResource):
    @cached_property
    def analytics(self) -> Analytics:
        return Analytics(self._client)

    @cached_property
    def deployments(self) -> Deployments:
        return Deployments(self._client)

    @cached_property
    def with_raw_response(self) -> ProjectsWithRawResponse:
        return ProjectsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectsWithStreamingResponse:
        return ProjectsWithStreamingResponse(self)

    def update(
        self,
        project_id: str,
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
        Update project details

        Args:
          description: The description of the project to be updated to. If this is `null`, no update
              will be made to the project description.

          name: The name of the project to be updated to. This must be globally unique. If this
              is `null`, no update will be made to the project name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._patch(
            f"/projects/{project_id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                project_update_params.ProjectUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Project,
        )

    def delete(
        self,
        project_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a project

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/projects/{project_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get(
        self,
        project_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Project:
        """
        Get project details

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._get(
            f"/projects/{project_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Project,
        )


class AsyncProjects(AsyncAPIResource):
    @cached_property
    def analytics(self) -> AsyncAnalytics:
        return AsyncAnalytics(self._client)

    @cached_property
    def deployments(self) -> AsyncDeployments:
        return AsyncDeployments(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProjectsWithRawResponse:
        return AsyncProjectsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectsWithStreamingResponse:
        return AsyncProjectsWithStreamingResponse(self)

    async def update(
        self,
        project_id: str,
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
        Update project details

        Args:
          description: The description of the project to be updated to. If this is `null`, no update
              will be made to the project description.

          name: The name of the project to be updated to. This must be globally unique. If this
              is `null`, no update will be made to the project name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._patch(
            f"/projects/{project_id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                project_update_params.ProjectUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Project,
        )

    async def delete(
        self,
        project_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a project

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/projects/{project_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get(
        self,
        project_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Project:
        """
        Get project details

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._get(
            f"/projects/{project_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Project,
        )


class ProjectsWithRawResponse:
    def __init__(self, projects: Projects) -> None:
        self._projects = projects

        self.update = to_raw_response_wrapper(
            projects.update,
        )
        self.delete = to_raw_response_wrapper(
            projects.delete,
        )
        self.get = to_raw_response_wrapper(
            projects.get,
        )

    @cached_property
    def analytics(self) -> AnalyticsWithRawResponse:
        return AnalyticsWithRawResponse(self._projects.analytics)

    @cached_property
    def deployments(self) -> DeploymentsWithRawResponse:
        return DeploymentsWithRawResponse(self._projects.deployments)


class AsyncProjectsWithRawResponse:
    def __init__(self, projects: AsyncProjects) -> None:
        self._projects = projects

        self.update = async_to_raw_response_wrapper(
            projects.update,
        )
        self.delete = async_to_raw_response_wrapper(
            projects.delete,
        )
        self.get = async_to_raw_response_wrapper(
            projects.get,
        )

    @cached_property
    def analytics(self) -> AsyncAnalyticsWithRawResponse:
        return AsyncAnalyticsWithRawResponse(self._projects.analytics)

    @cached_property
    def deployments(self) -> AsyncDeploymentsWithRawResponse:
        return AsyncDeploymentsWithRawResponse(self._projects.deployments)


class ProjectsWithStreamingResponse:
    def __init__(self, projects: Projects) -> None:
        self._projects = projects

        self.update = to_streamed_response_wrapper(
            projects.update,
        )
        self.delete = to_streamed_response_wrapper(
            projects.delete,
        )
        self.get = to_streamed_response_wrapper(
            projects.get,
        )

    @cached_property
    def analytics(self) -> AnalyticsWithStreamingResponse:
        return AnalyticsWithStreamingResponse(self._projects.analytics)

    @cached_property
    def deployments(self) -> DeploymentsWithStreamingResponse:
        return DeploymentsWithStreamingResponse(self._projects.deployments)


class AsyncProjectsWithStreamingResponse:
    def __init__(self, projects: AsyncProjects) -> None:
        self._projects = projects

        self.update = async_to_streamed_response_wrapper(
            projects.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            projects.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            projects.get,
        )

    @cached_property
    def analytics(self) -> AsyncAnalyticsWithStreamingResponse:
        return AsyncAnalyticsWithStreamingResponse(self._projects.analytics)

    @cached_property
    def deployments(self) -> AsyncDeploymentsWithStreamingResponse:
        return AsyncDeploymentsWithStreamingResponse(self._projects.deployments)
