"""Module handling NASA Earthdata credentials"""

import os

import earthaccess
from prefect.blocks.core import Block
from pydantic import VERSION as PYDANTIC_VERSION

if PYDANTIC_VERSION.startswith("2."):
    from pydantic.v1 import Field, SecretStr
else:
    from pydantic import Field, SecretStr


class EarthdataCredentials(Block):
    """
    Block used to manage authentication with NASA Earthdata.
    To obtain an account, please refer to the
    [Earthdata Login docs](https://www.earthdata.nasa.gov/eosdis/science-system-description/eosdis-components/earthdata-login).

    Authentication is handled via the `earthaccess` module.
    Refer to the [earthaccess docs](https://nsidc.github.io/earthaccess/)
    for more info about the possible credential configurations.

    Args:
        earthdata_username (str): The Earthdata username of a specific account.
        earthdata_password (str): The Earthdata password of a specific account.

    Example:
        Load stored Earthdata credentials:
        ```python
        from prefect_earthdata import EarthdataCredentials

        ed_credentials_block = EarthdataCredentials.load("BLOCK_NAME")
        ```
    """  # noqa E501

    _logo_url = "https://yt3.googleusercontent.com/ytc/AGIKgqPjIUeAw3_hrkHWZgixdwD5jc-hTWweoCA6bJMhUg=s176-c-k-c0x00ffffff-no-rj"  # noqa
    _block_type_name = "NASA Earthdata Credentials"
    _documentation_url = "https://giorgiobasile.github.io/prefect-earthdata/credentials/#prefect_earthdata.credentials.EarthdataCredentials"  # noqa

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
            from prefect_earthdata import EarthdataCredentials

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
