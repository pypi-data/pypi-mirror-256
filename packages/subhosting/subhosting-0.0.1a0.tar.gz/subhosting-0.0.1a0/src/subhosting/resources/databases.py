# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import database_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)
from ..types.shared import KvDatabase

__all__ = ["Databases", "AsyncDatabases"]


class Databases(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DatabasesWithRawResponse:
        return DatabasesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DatabasesWithStreamingResponse:
        return DatabasesWithStreamingResponse(self)

    def update(
        self,
        database_id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> KvDatabase:
        """
        Update KV database details

        Args:
          description: The description of the KV database to be updated to. If this is `null`, no
              update will be made to the KV database description.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not database_id:
            raise ValueError(f"Expected a non-empty value for `database_id` but received {database_id!r}")
        return self._patch(
            f"/databases/{database_id}",
            body=maybe_transform({"description": description}, database_update_params.DatabaseUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=KvDatabase,
        )


class AsyncDatabases(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDatabasesWithRawResponse:
        return AsyncDatabasesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDatabasesWithStreamingResponse:
        return AsyncDatabasesWithStreamingResponse(self)

    async def update(
        self,
        database_id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> KvDatabase:
        """
        Update KV database details

        Args:
          description: The description of the KV database to be updated to. If this is `null`, no
              update will be made to the KV database description.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not database_id:
            raise ValueError(f"Expected a non-empty value for `database_id` but received {database_id!r}")
        return await self._patch(
            f"/databases/{database_id}",
            body=maybe_transform({"description": description}, database_update_params.DatabaseUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=KvDatabase,
        )


class DatabasesWithRawResponse:
    def __init__(self, databases: Databases) -> None:
        self._databases = databases

        self.update = to_raw_response_wrapper(
            databases.update,
        )


class AsyncDatabasesWithRawResponse:
    def __init__(self, databases: AsyncDatabases) -> None:
        self._databases = databases

        self.update = async_to_raw_response_wrapper(
            databases.update,
        )


class DatabasesWithStreamingResponse:
    def __init__(self, databases: Databases) -> None:
        self._databases = databases

        self.update = to_streamed_response_wrapper(
            databases.update,
        )


class AsyncDatabasesWithStreamingResponse:
    def __init__(self, databases: AsyncDatabases) -> None:
        self._databases = databases

        self.update = async_to_streamed_response_wrapper(
            databases.update,
        )
