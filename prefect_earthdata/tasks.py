"""Module handling Prefect tasks interacting with NASA Earthdata"""

from typing import List

import earthaccess
from prefect import get_run_logger, task

from prefect_earthdata.credentials import EarthdataCredentials


@task
async def search_data(
    credentials: EarthdataCredentials, *args, **kwargs
) -> List[earthaccess.results.DataGranule]:
    """
    Searches for data on NASA Earthdata using the
    [`earthaccess.search_data()`](https://nsidc.github.io/earthaccess/user-reference/api/api/#earthaccess.api.search_data) function

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
        from prefect_earthdata.credentials import EarthdataCredentials
        from prefect_earthdata.tasks import search_data

        @flow
        def example_earthdata_search_flow():

            earthdata_credentials = EarthdataCredentials(
                earthdata_userame = "username",
                earthdata_password = "password"
            )

            granules = search_data(
                earthdata_credentials,
                count=1,
                short_name="ATL08",
                bounding_box=(-92.86, 16.26, -91.58, 16.97),
            )
            return granules

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
async def download(credentials: EarthdataCredentials, *args, **kwargs) -> List[str]:
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
        List of downloaded files.

    Example:
        Searches and downloads granules through NASA Earthdata.

        ```python
        from prefect import flow
        from prefect_earthdata.credentials import EarthdataCredentials
        from prefect_earthdata.tasks import search_data, download

        @flow
        def example_earthdata_download_flow():

            earthdata_credentials = EarthdataCredentials(
                earthdata_userame = "username",
                earthdata_password = "password"
            )

            granules = search_data(
                earthdata_credentials,
                count=1,
                short_name="ATL08",
                bounding_box=(-92.86, 16.26, -91.58, 16.97),
            )

            download_path = "/tmp"

            files = download(
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
