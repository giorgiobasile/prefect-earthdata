import pytest
import requests_mock
from earthaccess import Auth

from prefect_eo.earthdata import EarthdataCredentials


@pytest.fixture
def mock_earthdata_responses():
    with requests_mock.Mocker() as m:
        json_response = [
            {"access_token": "EDL-token-1", "expiration_date": "12/15/2023"},
            {"access_token": "EDL-token-2", "expiration_date": "12/16/2023"},
        ]
        m.get(
            "https://urs.earthdata.nasa.gov/api/users/tokens",
            json=json_response,
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
        yield m


def test_earthdata_credentials_login(mock_earthdata_responses):  # noqa
    """
    Asserts that instantiated EarthdataCredentials block creates an
    authenticated session.
    """

    # Set up mock user input
    mock_username = "user"
    mock_password = "password"

    # Instantiate EarthdataCredentials block
    earthdata_credentials_block = EarthdataCredentials(
        earthdata_username=mock_username, earthdata_password=mock_password
    )
    earthdata_auth = earthdata_credentials_block.login()

    assert isinstance(earthdata_auth, Auth)
    assert earthdata_auth.authenticated
