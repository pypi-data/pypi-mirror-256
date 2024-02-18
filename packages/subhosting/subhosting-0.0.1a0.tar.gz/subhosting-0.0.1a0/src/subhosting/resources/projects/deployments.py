# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Dict, Optional

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
from ...types.shared import Deployment
from ...types.projects import DeploymentListResponse, deployment_list_params, deployment_create_params

__all__ = ["Deployments", "AsyncDeployments"]


class Deployments(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeploymentsWithRawResponse:
        return DeploymentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeploymentsWithStreamingResponse:
        return DeploymentsWithStreamingResponse(self)

    def create(
        self,
        project_id: str,
        *,
        assets: Dict[str, deployment_create_params.Assets],
        entry_point_url: str,
        env_vars: Dict[str, str],
        compiler_options: deployment_create_params.CompilerOptions | NotGiven = NOT_GIVEN,
        databases: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        import_map_url: Optional[str] | NotGiven = NOT_GIVEN,
        lock_file_url: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Deployment:
        """
        Create a deployment

        This API initiates a build process for a new deployment.

        Note that this process is asynchronous; the completion of this API doesn't mean
        the deployment is ready. In order to keep track of the progress of the build,
        call the "Get build logs of a deployment" API or the "Get deployment details"
        API.

        Args:
          assets: A map whose key represents a file path, and the value is an asset that composes
              the deployment.

              Each asset is one of the following three kinds:

              1. A file with content data (which is UTF-8 for text, or base64 for binary)
              2. A file with a hash
              3. A symbolic link to another asset

              Assets that were uploaded in some of the previous deployments don't need to be
              uploaded again. In this case, in order to identify the asset, just provide the
              SHA-1 hash of the content.

          entry_point_url: An URL of the entry point of the application. This is the file that will be
              executed when the deployment is invoked.

          env_vars: A dictionary of environment variables to be set in the runtime environment of
              the deployment.

          compiler_options: Compiler options to be used when building the deployment.

              If `null` is given, Deno's config file (i.e. `deno.json` or `deno.jsonc`) will
              be auto-discovered, which may contain a `compilerOptions` field. If found, that
              compiler options will be applied.

              If an empty object `{}` is given,
              [the default compiler options](https://docs.deno.com/runtime/manual/advanced/typescript/configuration#how-deno-uses-a-configuration-file)
              will be applied.

          databases: KV database ID mappings to associate with the deployment.

              A key represents a KV database name (e.g. `"default"`), and a value is a KV
              database ID.

              Currently, only `"default"` database is supported. If any other database name is
              specified, that will be rejected.

              If not provided, the deployment will be created with no KV database attached.

          description: A description of the created deployment. If not provided, an empty string will
              be set.

          import_map_url: An URL of the import map file.

              If `null` is given, import map auto-discovery logic will be performed, where it
              looks for Deno's config file (i.e. `deno.json` or `deno.jsonc`) which may
              contain an embedded import map or a path to an import map file. If found, that
              import map will be used.

              If an empty string is given, no import map will be used.

          lock_file_url: An URL of the lock file.

              If `null` is given, lock file auto-discovery logic will be performed, where it
              looks for Deno's config file (i.e. `deno.json` or `deno.jsonc`) which may
              contain a path to a lock file or boolean value, such as `"lock": false` or
              `"lock": "my-lock.lock"`. If a config file is found, the semantics of the lock
              field is the same as the Deno CLI, so refer to
              [the CLI doc page](https://docs.deno.com/runtime/manual/basics/modules/integrity_checking#auto-generated-lockfile).

              If an empty string is given, no lock file will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._post(
            f"/projects/{project_id}/deployments",
            body=maybe_transform(
                {
                    "assets": assets,
                    "entry_point_url": entry_point_url,
                    "env_vars": env_vars,
                    "compiler_options": compiler_options,
                    "databases": databases,
                    "description": description,
                    "import_map_url": import_map_url,
                    "lock_file_url": lock_file_url,
                },
                deployment_create_params.DeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Deployment,
        )

    def list(
        self,
        project_id: str,
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
    ) -> DeploymentListResponse:
        """
        List deployments of a project

        This API returns a list of deployments belonging to the specified project in a
        pagenated manner.

        The URLs for the next, previous, first, and last page are returned in the `Link`
        header of the response, if any.

        Args:
          limit: The maximum number of items to return per page.

          order: Sort order, either `asc` or `desc`. Defaults to `asc`.

          page: The page number to return.

          q: Query by deployment ID

          sort: The field to sort by, either `id` or `created_at`. Defaults to `created_at`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._get(
            f"/projects/{project_id}/deployments",
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
                    deployment_list_params.DeploymentListParams,
                ),
            ),
            cast_to=DeploymentListResponse,
        )


class AsyncDeployments(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeploymentsWithRawResponse:
        return AsyncDeploymentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeploymentsWithStreamingResponse:
        return AsyncDeploymentsWithStreamingResponse(self)

    async def create(
        self,
        project_id: str,
        *,
        assets: Dict[str, deployment_create_params.Assets],
        entry_point_url: str,
        env_vars: Dict[str, str],
        compiler_options: deployment_create_params.CompilerOptions | NotGiven = NOT_GIVEN,
        databases: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        import_map_url: Optional[str] | NotGiven = NOT_GIVEN,
        lock_file_url: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Deployment:
        """
        Create a deployment

        This API initiates a build process for a new deployment.

        Note that this process is asynchronous; the completion of this API doesn't mean
        the deployment is ready. In order to keep track of the progress of the build,
        call the "Get build logs of a deployment" API or the "Get deployment details"
        API.

        Args:
          assets: A map whose key represents a file path, and the value is an asset that composes
              the deployment.

              Each asset is one of the following three kinds:

              1. A file with content data (which is UTF-8 for text, or base64 for binary)
              2. A file with a hash
              3. A symbolic link to another asset

              Assets that were uploaded in some of the previous deployments don't need to be
              uploaded again. In this case, in order to identify the asset, just provide the
              SHA-1 hash of the content.

          entry_point_url: An URL of the entry point of the application. This is the file that will be
              executed when the deployment is invoked.

          env_vars: A dictionary of environment variables to be set in the runtime environment of
              the deployment.

          compiler_options: Compiler options to be used when building the deployment.

              If `null` is given, Deno's config file (i.e. `deno.json` or `deno.jsonc`) will
              be auto-discovered, which may contain a `compilerOptions` field. If found, that
              compiler options will be applied.

              If an empty object `{}` is given,
              [the default compiler options](https://docs.deno.com/runtime/manual/advanced/typescript/configuration#how-deno-uses-a-configuration-file)
              will be applied.

          databases: KV database ID mappings to associate with the deployment.

              A key represents a KV database name (e.g. `"default"`), and a value is a KV
              database ID.

              Currently, only `"default"` database is supported. If any other database name is
              specified, that will be rejected.

              If not provided, the deployment will be created with no KV database attached.

          description: A description of the created deployment. If not provided, an empty string will
              be set.

          import_map_url: An URL of the import map file.

              If `null` is given, import map auto-discovery logic will be performed, where it
              looks for Deno's config file (i.e. `deno.json` or `deno.jsonc`) which may
              contain an embedded import map or a path to an import map file. If found, that
              import map will be used.

              If an empty string is given, no import map will be used.

          lock_file_url: An URL of the lock file.

              If `null` is given, lock file auto-discovery logic will be performed, where it
              looks for Deno's config file (i.e. `deno.json` or `deno.jsonc`) which may
              contain a path to a lock file or boolean value, such as `"lock": false` or
              `"lock": "my-lock.lock"`. If a config file is found, the semantics of the lock
              field is the same as the Deno CLI, so refer to
              [the CLI doc page](https://docs.deno.com/runtime/manual/basics/modules/integrity_checking#auto-generated-lockfile).

              If an empty string is given, no lock file will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._post(
            f"/projects/{project_id}/deployments",
            body=maybe_transform(
                {
                    "assets": assets,
                    "entry_point_url": entry_point_url,
                    "env_vars": env_vars,
                    "compiler_options": compiler_options,
                    "databases": databases,
                    "description": description,
                    "import_map_url": import_map_url,
                    "lock_file_url": lock_file_url,
                },
                deployment_create_params.DeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Deployment,
        )

    async def list(
        self,
        project_id: str,
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
    ) -> DeploymentListResponse:
        """
        List deployments of a project

        This API returns a list of deployments belonging to the specified project in a
        pagenated manner.

        The URLs for the next, previous, first, and last page are returned in the `Link`
        header of the response, if any.

        Args:
          limit: The maximum number of items to return per page.

          order: Sort order, either `asc` or `desc`. Defaults to `asc`.

          page: The page number to return.

          q: Query by deployment ID

          sort: The field to sort by, either `id` or `created_at`. Defaults to `created_at`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._get(
            f"/projects/{project_id}/deployments",
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
                    deployment_list_params.DeploymentListParams,
                ),
            ),
            cast_to=DeploymentListResponse,
        )


class DeploymentsWithRawResponse:
    def __init__(self, deployments: Deployments) -> None:
        self._deployments = deployments

        self.create = to_raw_response_wrapper(
            deployments.create,
        )
        self.list = to_raw_response_wrapper(
            deployments.list,
        )


class AsyncDeploymentsWithRawResponse:
    def __init__(self, deployments: AsyncDeployments) -> None:
        self._deployments = deployments

        self.create = async_to_raw_response_wrapper(
            deployments.create,
        )
        self.list = async_to_raw_response_wrapper(
            deployments.list,
        )


class DeploymentsWithStreamingResponse:
    def __init__(self, deployments: Deployments) -> None:
        self._deployments = deployments

        self.create = to_streamed_response_wrapper(
            deployments.create,
        )
        self.list = to_streamed_response_wrapper(
            deployments.list,
        )


class AsyncDeploymentsWithStreamingResponse:
    def __init__(self, deployments: AsyncDeployments) -> None:
        self._deployments = deployments

        self.create = async_to_streamed_response_wrapper(
            deployments.create,
        )
        self.list = async_to_streamed_response_wrapper(
            deployments.list,
        )
