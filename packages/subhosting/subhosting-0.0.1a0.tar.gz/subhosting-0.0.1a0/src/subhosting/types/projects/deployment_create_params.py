# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["DeploymentCreateParams", "Assets", "AssetsFile", "AssetsSymlink", "CompilerOptions"]


class DeploymentCreateParams(TypedDict, total=False):
    assets: Required[Dict[str, Assets]]
    """
    A map whose key represents a file path, and the value is an asset that composes
    the deployment.

    Each asset is one of the following three kinds:

    1. A file with content data (which is UTF-8 for text, or base64 for binary)
    2. A file with a hash
    3. A symbolic link to another asset

    Assets that were uploaded in some of the previous deployments don't need to be
    uploaded again. In this case, in order to identify the asset, just provide the
    SHA-1 hash of the content.
    """

    entry_point_url: Required[Annotated[str, PropertyInfo(alias="entryPointUrl")]]
    """
    An URL of the entry point of the application. This is the file that will be
    executed when the deployment is invoked.
    """

    env_vars: Required[Annotated[Dict[str, str], PropertyInfo(alias="envVars")]]
    """
    A dictionary of environment variables to be set in the runtime environment of
    the deployment.
    """

    compiler_options: Annotated[CompilerOptions, PropertyInfo(alias="compilerOptions")]
    """Compiler options to be used when building the deployment.

    If `null` is given, Deno's config file (i.e. `deno.json` or `deno.jsonc`) will
    be auto-discovered, which may contain a `compilerOptions` field. If found, that
    compiler options will be applied.

    If an empty object `{}` is given,
    [the default compiler options](https://docs.deno.com/runtime/manual/advanced/typescript/configuration#how-deno-uses-a-configuration-file)
    will be applied.
    """

    databases: Optional[Dict[str, str]]
    """KV database ID mappings to associate with the deployment.

    A key represents a KV database name (e.g. `"default"`), and a value is a KV
    database ID.

    Currently, only `"default"` database is supported. If any other database name is
    specified, that will be rejected.

    If not provided, the deployment will be created with no KV database attached.
    """

    description: Optional[str]
    """A description of the created deployment.

    If not provided, an empty string will be set.
    """

    import_map_url: Annotated[Optional[str], PropertyInfo(alias="importMapUrl")]
    """An URL of the import map file.

    If `null` is given, import map auto-discovery logic will be performed, where it
    looks for Deno's config file (i.e. `deno.json` or `deno.jsonc`) which may
    contain an embedded import map or a path to an import map file. If found, that
    import map will be used.

    If an empty string is given, no import map will be used.
    """

    lock_file_url: Annotated[Optional[str], PropertyInfo(alias="lockFileUrl")]
    """An URL of the lock file.

    If `null` is given, lock file auto-discovery logic will be performed, where it
    looks for Deno's config file (i.e. `deno.json` or `deno.jsonc`) which may
    contain a path to a lock file or boolean value, such as `"lock": false` or
    `"lock": "my-lock.lock"`. If a config file is found, the semantics of the lock
    field is the same as the Deno CLI, so refer to
    [the CLI doc page](https://docs.deno.com/runtime/manual/basics/modules/integrity_checking#auto-generated-lockfile).

    If an empty string is given, no lock file will be used.
    """


class AssetsFile(TypedDict, total=False):
    kind: Required[Literal["file"]]

    content: str

    encoding: Literal["utf-8", "base64"]

    git_sha1: Annotated[str, PropertyInfo(alias="gitSha1")]


class AssetsSymlink(TypedDict, total=False):
    kind: Required[Literal["symlink"]]

    target: Required[str]


Assets = Union[AssetsFile, AssetsSymlink]


class CompilerOptions(TypedDict, total=False):
    jsx: Optional[str]

    jsx_factory: Annotated[Optional[str], PropertyInfo(alias="jsxFactory")]

    jsx_fragment_factory: Annotated[Optional[str], PropertyInfo(alias="jsxFragmentFactory")]

    jsx_import_source: Annotated[Optional[str], PropertyInfo(alias="jsxImportSource")]
