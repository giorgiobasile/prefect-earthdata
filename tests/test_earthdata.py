import json
import tempfile
from pathlib import Path

import pytest
import requests_mock
from earthaccess import Auth
from importlib_resources import open_binary, open_text
from prefect import flow
from prefect.testing.utilities import prefect_test_harness

from prefect_eo.earthdata import (
    EarthdataCredentials,
    earthdata_download,
    earthdata_search_data,
)


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

        with open_text(
            "tests.data", "earthdata_search_response.json"
        ) as search_data_response_file:
            search_data_response = json.load(search_data_response_file)

        m.get(
            "https://cmr.earthdata.nasa.gov/search/granules.umm_json?short_name=ATL08&bounding_box=-92.86,16.26,-91.58,16.97",  # noqa E501
            headers={"CMR-Hits": "760"},
            json=search_data_response,
            status_code=200,
        )

        with open_binary("tests.data", "empty.h5") as download_response_file:
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


def test_earthdata_credentials_login(mock_earthdata_responses):  # noqa

    mock_username = "user"
    mock_password = "password"

    earthdata_credentials_block = EarthdataCredentials(
        earthdata_username=mock_username, earthdata_password=mock_password
    )
    earthdata_auth = earthdata_credentials_block.login()

    assert isinstance(earthdata_auth, Auth)
    assert earthdata_auth.authenticated


def test_earthdata_search_data_and_download(earthdata_credentials_mock):  # noqa
    @flow
    def test_flow(download_path):
        granules = earthdata_search_data(
            earthdata_credentials_mock,
            count=1,
            short_name="ATL08",
            bounding_box=(-92.86, 16.26, -91.58, 16.97),
        )
        files = earthdata_download(earthdata_credentials_mock, granules, download_path)

        return granules, files

    with tempfile.TemporaryDirectory() as temp_dir:
        with prefect_test_harness():
            granules, files = test_flow(temp_dir)
            assert isinstance(granules, list)
            assert len(granules) == 1
            assert files == ["ATL08_20181105083647_05760107_005_01.h5"]
            assert Path(temp_dir, "ATL08_20181105083647_05760107_005_01.h5").exists()
