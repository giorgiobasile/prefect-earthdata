from prefect import flow

from prefect_eo.tasks import (
    goodbye_prefect_eo,
    hello_prefect_eo,
)


def test_hello_prefect_eo():
    @flow
    def test_flow():
        return hello_prefect_eo()

    result = test_flow()
    assert result == "Hello, prefect-eo!"


def goodbye_hello_prefect_eo():
    @flow
    def test_flow():
        return goodbye_prefect_eo()

    result = test_flow()
    assert result == "Goodbye, prefect-eo!"
