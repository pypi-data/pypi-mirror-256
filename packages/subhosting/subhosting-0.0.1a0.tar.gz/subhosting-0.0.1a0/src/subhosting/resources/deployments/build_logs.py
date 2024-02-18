# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ...types.deployments import BuildLogGetResponse

__all__ = ["BuildLogs", "AsyncBuildLogs"]


class BuildLogs(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BuildLogsWithRawResponse:
        return BuildLogsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BuildLogsWithStreamingResponse:
        return BuildLogsWithStreamingResponse(self)

    def get(
        self,
        deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BuildLogGetResponse:
        """
        Get build logs of a deployment

        This API returns build logs of the specified deployment. It's useful to watch
        the build progress, figure out what went wrong in case of a build failure, and
        so on.

        The response format can be controlled by the `Accept` header; if
        `application/x-ndjson` is specified, the response will be a stream of
        newline-delimited JSON objects. Otherwise it will be a JSON array of objects.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._get(
            f"/deployments/{deployment_id}/build_logs",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuildLogGetResponse,
        )


class AsyncBuildLogs(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBuildLogsWithRawResponse:
        return AsyncBuildLogsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBuildLogsWithStreamingResponse:
        return AsyncBuildLogsWithStreamingResponse(self)

    async def get(
        self,
        deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BuildLogGetResponse:
        """
        Get build logs of a deployment

        This API returns build logs of the specified deployment. It's useful to watch
        the build progress, figure out what went wrong in case of a build failure, and
        so on.

        The response format can be controlled by the `Accept` header; if
        `application/x-ndjson` is specified, the response will be a stream of
        newline-delimited JSON objects. Otherwise it will be a JSON array of objects.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._get(
            f"/deployments/{deployment_id}/build_logs",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuildLogGetResponse,
        )


class BuildLogsWithRawResponse:
    def __init__(self, build_logs: BuildLogs) -> None:
        self._build_logs = build_logs

        self.get = to_raw_response_wrapper(
            build_logs.get,
        )


class AsyncBuildLogsWithRawResponse:
    def __init__(self, build_logs: AsyncBuildLogs) -> None:
        self._build_logs = build_logs

        self.get = async_to_raw_response_wrapper(
            build_logs.get,
        )


class BuildLogsWithStreamingResponse:
    def __init__(self, build_logs: BuildLogs) -> None:
        self._build_logs = build_logs

        self.get = to_streamed_response_wrapper(
            build_logs.get,
        )


class AsyncBuildLogsWithStreamingResponse:
    def __init__(self, build_logs: AsyncBuildLogs) -> None:
        self._build_logs = build_logs

        self.get = async_to_streamed_response_wrapper(
            build_logs.get,
        )
