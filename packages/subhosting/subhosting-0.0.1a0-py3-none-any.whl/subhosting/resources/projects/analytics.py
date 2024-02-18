# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union
from datetime import datetime

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
from ...types.shared import analytics
from ...types.projects import analytics_get_params

__all__ = ["Analytics", "AsyncAnalytics"]


class Analytics(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AnalyticsWithRawResponse:
        return AnalyticsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnalyticsWithStreamingResponse:
        return AnalyticsWithStreamingResponse(self)

    def get(
        self,
        project_id: str,
        *,
        since: Union[str, datetime],
        until: Union[str, datetime],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> analytics.Analytics:
        """Retrieve project analytics

        This API returns analytics for the specified project.

        The analytics are returned
        as time series data in 15 minute intervals, with the `time` field representing
        the start of the interval.

        Args:
          since: Start of the time range in RFC3339 format.

              Defaults to 24 hours ago.

          until: End of the time range in RFC3339 format.

              Defaults to the current time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._get(
            f"/projects/{project_id}/analytics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "since": since,
                        "until": until,
                    },
                    analytics_get_params.AnalyticsGetParams,
                ),
            ),
            cast_to=analytics.Analytics,
        )


class AsyncAnalytics(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAnalyticsWithRawResponse:
        return AsyncAnalyticsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnalyticsWithStreamingResponse:
        return AsyncAnalyticsWithStreamingResponse(self)

    async def get(
        self,
        project_id: str,
        *,
        since: Union[str, datetime],
        until: Union[str, datetime],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> analytics.Analytics:
        """Retrieve project analytics

        This API returns analytics for the specified project.

        The analytics are returned
        as time series data in 15 minute intervals, with the `time` field representing
        the start of the interval.

        Args:
          since: Start of the time range in RFC3339 format.

              Defaults to 24 hours ago.

          until: End of the time range in RFC3339 format.

              Defaults to the current time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._get(
            f"/projects/{project_id}/analytics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "since": since,
                        "until": until,
                    },
                    analytics_get_params.AnalyticsGetParams,
                ),
            ),
            cast_to=analytics.Analytics,
        )


class AnalyticsWithRawResponse:
    def __init__(self, analytics: Analytics) -> None:
        self._analytics = analytics

        self.get = to_raw_response_wrapper(
            analytics.get,
        )


class AsyncAnalyticsWithRawResponse:
    def __init__(self, analytics: AsyncAnalytics) -> None:
        self._analytics = analytics

        self.get = async_to_raw_response_wrapper(
            analytics.get,
        )


class AnalyticsWithStreamingResponse:
    def __init__(self, analytics: Analytics) -> None:
        self._analytics = analytics

        self.get = to_streamed_response_wrapper(
            analytics.get,
        )


class AsyncAnalyticsWithStreamingResponse:
    def __init__(self, analytics: AsyncAnalytics) -> None:
        self._analytics = analytics

        self.get = async_to_streamed_response_wrapper(
            analytics.get,
        )
