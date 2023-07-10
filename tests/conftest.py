import json

import pytest
import requests_mock
from importlib_resources import files
from prefect.testing.utilities import prefect_test_harness

from prefect_earthdata.credentials import EarthdataCredentials


def pytest_configure(config):
    config.addinivalue_line("markers", "flaky: mark test as flaky")


@pytest.fixture(scope="session", autouse=True)
def prefect_db():
    """
    Sets up test harness for temporary DB during test runs.
    """
    with prefect_test_harness():
        yield


@pytest.fixture(autouse=True)
def reset_object_registry():
    """
    Ensures each test has a clean object registry.
    """
    from prefect.context import PrefectObjectRegistry

    with PrefectObjectRegistry():
        yield


@pytest.fixture
def mock_earthdata_responses():
    with requests_mock.Mocker() as m:

        m.get(
            "https://urs.earthdata.nasa.gov/api/users/tokens",
            json=[
                {"access_token": "EDL-token-1", "expiration_date": "12/15/2023"},
                {"access_token": "EDL-token-2", "expiration_date": "12/16/2023"},
            ],
            status_code=200,
        )
        m.get(
            "https://urs.earthdata.nasa.gov/profile",
            json={"uid": "test_username"},
            status_code=200,
        )
        m.get(
            "https://urs.earthdata.nasa.gov/api/users/user?client_id=ntD0YGC_SM3Bjs-Tnxd7bg",  # noqa E501
            json={"uid": "test_username"},
            status_code=200,
        )

        with files("tests.data").joinpath("earthdata_search_response.json").open(
            "r"
        ) as search_data_response_file:
            search_data_response = json.load(search_data_response_file)

        m.get(
            "https://cmr.earthdata.nasa.gov/search/granules.umm_json?short_name=ATL08&bounding_box=-92.86,16.26,-91.58,16.97",  # noqa E501
            headers={"CMR-Hits": "760"},
            json=search_data_response,
            status_code=200,
        )

        with files("tests.data").joinpath("empty.h5").open(
            "rb"
        ) as download_response_file:
            download_response = download_response_file.read()
        m.get(
            "https://data.nsidc.earthdatacloud.nasa.gov/nsidc-cumulus-prod-protected/ATLAS/ATL08/005/2018/11/05/ATL08_20181105083647_05760107_005_01.h5",  # noqa E501
            body=download_response,
            status_code=200,
        )
        yield m


@pytest.fixture
def earthdata_credentials_mock(mock_earthdata_responses):
    return EarthdataCredentials(
        earthdata_username="user", earthdata_password="password"
    )
