"""Module handling NASA Earthdata credentials"""

import os
from typing import List

import earthaccess
from prefect import get_run_logger, task
from prefect.blocks.core import Block
from pydantic import Field, SecretStr


class EarthdataCredentials(Block):
    """
    Block used to manage authentication with NASA Earthdata.
    NASA Earthdata authentication is handled via the `earthaccess` module.
    Refer to the [earthaccess docs](https://nsidc.github.io/earthaccess/)
    for more info about the possible credential configurations.

    Example:
        Load stored Earthdata credentials:
        ```python
        from prefect_eo import EarthdataCredentials

        ed_credentials_block = EarthdataCredentials.load("BLOCK_NAME")
        ```
    """  # noqa E501

    _logo_url = "https://yt3.googleusercontent.com/ytc/AGIKgqPjIUeAw3_hrkHWZgixdwD5jc-hTWweoCA6bJMhUg=s176-c-k-c0x00ffffff-no-rj"  # noqa
    _block_type_name = "NASA Earthdata Credentials"
    _documentation_url = "https://nsidc.github.io/earthaccess/"  # noqa

    earthdata_username: str = Field(
        default=...,
        description="The Earthdata username of a specific account.",
        title="Earthdata username",
    )
    earthdata_password: SecretStr = Field(
        default=...,
        description="The Earthdata password of a specific account.",
        title="Earthdata password",
    )

    def login(self) -> earthaccess.Auth:
        """
        Returns an authenticated session with NASA Earthdata using
        the [`earthaccess.login()`](https://nsidc.github.io/earthaccess/user-reference/api/api/#earthaccess.api.login) function

        Example:
            Authenticates with NASA Earthdata using the credentials.

            ```python
            from prefect_eo.earthdata import EarthdataCredentials

            earthdata_credentials_block = EarthdataCredentials(
                earthdata_username = "username",
                earthdata_password = "password"
            )
            earthdata_auth = earthdata_credentials_block.login()
            ```
        """  # noqa E501

        os.environ["EARTHDATA_USERNAME"] = self.earthdata_username
        os.environ["EARTHDATA_PASSWORD"] = self.earthdata_password.get_secret_value()
        return earthaccess.login(strategy="environment")


@task
async def earthdata_search_data(
    credentials: EarthdataCredentials, *args, **kwargs
) -> List[earthaccess.results.DataGranule]:
    """
    Searches for data on NASA Earthdata using the
    c function

    Args:
        credentials: An `EarthdataCredentials` object used
            to authenticate with NASA Earthdata.
        args: Additional positional arguments to be passed
            to `earthaccess.search_data()`.
        kwargs: Additional keyword arguments to be passed
            to `earthaccess.search_data()`.

    Returns:
        A list of `DataGranule` objects representing the search results.

    Example:
        Searches granules through NASA Earthdata.

        ```python
        from prefect import flow
        from prefect_eo.earthdata import EarthdataCredentials
        from prefect_eo.earthdata import earthdata_search_data

        @flow
        def example_earthdata_search_flow():

            credentials = EarthdataCredentials(
                earthdata_userame = "username",
                earthdata_password = "password"
            )

            search_results = earthdata_search_data(
                earthdata_credentials,
                count=1,
                short_name="ATL08",
                bounding_box=(-92.86, 16.26, -91.58, 16.97),
            )
            return search_results

        example_earthdata_search_flow()
        ```
    """  # noqa: E501

    logger = get_run_logger()

    logger.debug("Authenticating to NASA Earthdata")
    auth = credentials.login()
    if not auth.authenticated:
        raise ValueError("Could not authenticate to NASA Earthdata")

    return earthaccess.search_data(*args, **kwargs)


@task
async def earthdata_download(
    credentials: EarthdataCredentials, *args, **kwargs
) -> List[str]:
    """
    Downloads data from NASA Earthdata using the
    [`earthaccess.download()`](https://nsidc.github.io/earthaccess/user-reference/api/api/#earthaccess.api.download) function

    Args:
        credentials: An `EarthdataCredentials` object used
            to authenticate with NASA Earthdata.
        args: Additional positional arguments to be passed
            to `earthaccess.download()`.
        kwargs: Additional keyword arguments to be passed
            to `earthaccess.download()`.

    Returns:
        A list of `DataGranule` objects representing the search results.

    Example:
        Searches and downloads granules through NASA Earthdata.

        ```python
        from prefect import flow
        from prefect_eo.earthdata import EarthdataCredentials
        from prefect_eo.earthdata import earthdata_search_data

        @flow
        def example_earthdata_download_flow():

            credentials = EarthdataCredentials(
                earthdata_userame = "username",
                earthdata_password = "password"
            )

            search_results = earthdata_search_data(
                earthdata_credentials,
                count=1,
                short_name="ATL08",
                bounding_box=(-92.86, 16.26, -91.58, 16.97),
            )

            files = earthdata_download(
                earthdata_credentials,
                granules=granules,
                local_path=download_path
            )

            return granules, files

        example_earthdata_download_flow()
        ```
    """  # noqa: E501

    logger = get_run_logger()

    logger.debug("Authenticating to NASA Earthdata")
    auth = credentials.login()
    if not auth.authenticated:
        raise ValueError("Could not authenticate to NASA Earthdata")

    return earthaccess.download(*args, **kwargs)
