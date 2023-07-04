from earthaccess import Auth

from prefect_earthdata.credentials import EarthdataCredentials


def test_earthdata_credentials_login(mock_earthdata_responses):  # noqa

    mock_username = "user"
    mock_password = "password"

    earthdata_credentials_block = EarthdataCredentials(
        earthdata_username=mock_username, earthdata_password=mock_password
    )
    earthdata_auth = earthdata_credentials_block.login()

    assert isinstance(earthdata_auth, Auth)
    assert earthdata_auth.authenticated
