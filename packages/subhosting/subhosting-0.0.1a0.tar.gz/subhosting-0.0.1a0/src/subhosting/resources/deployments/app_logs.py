# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal

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
from ...types.deployments import AppLogGetResponse, app_log_get_params

__all__ = ["AppLogs", "AsyncAppLogs"]


class AppLogs(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AppLogsWithRawResponse:
        return AppLogsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AppLogsWithStreamingResponse:
        return AppLogsWithStreamingResponse(self)

    def get(
        self,
        deployment_id: str,
        *,
        cursor: Optional[str] | NotGiven = NOT_GIVEN,
        level: Literal["error", "warning", "info", "debug"] | NotGiven = NOT_GIVEN,
        limit: Optional[int] | NotGiven = NOT_GIVEN,
        order: Optional[str] | NotGiven = NOT_GIVEN,
        q: Optional[str] | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        since: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        sort: Optional[str] | NotGiven = NOT_GIVEN,
        until: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppLogGetResponse:
        """
        Get execution logs of a deployment

        This API can return either past logs or real-time logs depending on the presence
        of the since and until query parameters; if at least one of them is provided,
        past logs are returned, otherwise real-time logs are returned.

        Also, the response format can be controlled by the `Accept` header; if
        `application/x-ndjson` is specified, the response will be a stream of
        newline-delimited JSON objects. Otherwise it will be a JSON array of objects.

        Args:
          cursor: Opaque value that represents the cursor of the last log returned in the previous
              request.

              This is only effective for the past log mode.

          level: Log level(s) to filter logs by.

              Defaults to all levels (i.e. no filter applied).

              Multiple levels can be specified using comma-separated format.

          limit: Maximum number of logs to return in one request.

              This is only effective for the past log mode.

          order: Sort order, either `asc` or `desc`. Defaults to `desc`.

              For backward compatibility, `timeAsc` and `timeDesc` are also supported, but
              deprecated.

              This is only effective for the past log mode.

          q: Text to search for in log message.

          region: Region(s) to filter logs by.

              Defaults to all regions (i.e. no filter applied).

              Multiple regions can be specified using comma-separated format.

          since: Start time of the time range to filter logs by.

              Defaults to the Unix Epoch (though the log retention period is 2 weeks as of
              now).

              If neither `since` nor `until` is specified, real-time logs are returned.

          sort: The field to sort by. Currently only `time` is supported.

              This is only effective for the past log mode.

          until: End time of the time range to filter logs by.

              Defaults to the current time.

              If neither `since` nor `until` is specified, real-time logs are returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._get(
            f"/deployments/{deployment_id}/app_logs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "level": level,
                        "limit": limit,
                        "order": order,
                        "q": q,
                        "region": region,
                        "since": since,
                        "sort": sort,
                        "until": until,
                    },
                    app_log_get_params.AppLogGetParams,
                ),
            ),
            cast_to=AppLogGetResponse,
        )


class AsyncAppLogs(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAppLogsWithRawResponse:
        return AsyncAppLogsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAppLogsWithStreamingResponse:
        return AsyncAppLogsWithStreamingResponse(self)

    async def get(
        self,
        deployment_id: str,
        *,
        cursor: Optional[str] | NotGiven = NOT_GIVEN,
        level: Literal["error", "warning", "info", "debug"] | NotGiven = NOT_GIVEN,
        limit: Optional[int] | NotGiven = NOT_GIVEN,
        order: Optional[str] | NotGiven = NOT_GIVEN,
        q: Optional[str] | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        since: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        sort: Optional[str] | NotGiven = NOT_GIVEN,
        until: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppLogGetResponse:
        """
        Get execution logs of a deployment

        This API can return either past logs or real-time logs depending on the presence
        of the since and until query parameters; if at least one of them is provided,
        past logs are returned, otherwise real-time logs are returned.

        Also, the response format can be controlled by the `Accept` header; if
        `application/x-ndjson` is specified, the response will be a stream of
        newline-delimited JSON objects. Otherwise it will be a JSON array of objects.

        Args:
          cursor: Opaque value that represents the cursor of the last log returned in the previous
              request.

              This is only effective for the past log mode.

          level: Log level(s) to filter logs by.

              Defaults to all levels (i.e. no filter applied).

              Multiple levels can be specified using comma-separated format.

          limit: Maximum number of logs to return in one request.

              This is only effective for the past log mode.

          order: Sort order, either `asc` or `desc`. Defaults to `desc`.

              For backward compatibility, `timeAsc` and `timeDesc` are also supported, but
              deprecated.

              This is only effective for the past log mode.

          q: Text to search for in log message.

          region: Region(s) to filter logs by.

              Defaults to all regions (i.e. no filter applied).

              Multiple regions can be specified using comma-separated format.

          since: Start time of the time range to filter logs by.

              Defaults to the Unix Epoch (though the log retention period is 2 weeks as of
              now).

              If neither `since` nor `until` is specified, real-time logs are returned.

          sort: The field to sort by. Currently only `time` is supported.

              This is only effective for the past log mode.

          until: End time of the time range to filter logs by.

              Defaults to the current time.

              If neither `since` nor `until` is specified, real-time logs are returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._get(
            f"/deployments/{deployment_id}/app_logs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "level": level,
                        "limit": limit,
                        "order": order,
                        "q": q,
                        "region": region,
                        "since": since,
                        "sort": sort,
                        "until": until,
                    },
                    app_log_get_params.AppLogGetParams,
                ),
            ),
            cast_to=AppLogGetResponse,
        )


class AppLogsWithRawResponse:
    def __init__(self, app_logs: AppLogs) -> None:
        self._app_logs = app_logs

        self.get = to_raw_response_wrapper(
            app_logs.get,
        )


class AsyncAppLogsWithRawResponse:
    def __init__(self, app_logs: AsyncAppLogs) -> None:
        self._app_logs = app_logs

        self.get = async_to_raw_response_wrapper(
            app_logs.get,
        )


class AppLogsWithStreamingResponse:
    def __init__(self, app_logs: AppLogs) -> None:
        self._app_logs = app_logs

        self.get = to_streamed_response_wrapper(
            app_logs.get,
        )


class AsyncAppLogsWithStreamingResponse:
    def __init__(self, app_logs: AsyncAppLogs) -> None:
        self._app_logs = app_logs

        self.get = async_to_streamed_response_wrapper(
            app_logs.get,
        )
