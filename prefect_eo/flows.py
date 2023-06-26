"""This is an example flows module"""
from prefect import flow

from prefect_eo.blocks import EoBlock
from prefect_eo.tasks import (
    goodbye_prefect_eo,
    hello_prefect_eo,
)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    EoBlock.seed_value_for_example()
    block = EoBlock.load("sample-block")

    print(hello_prefect_eo())
    print(f"The block's value: {block.value}")
    print(goodbye_prefect_eo())
    return "Done"


if __name__ == "__main__":
    hello_and_goodbye()
