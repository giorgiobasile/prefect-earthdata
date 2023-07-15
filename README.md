# prefect-earthdata

<p align="center">
    <!--- Insert a cover image here -->
    <!--- <br> -->
    <a href="https://pypi.python.org/pypi/prefect-earthdata/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-earthdata?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/giorgiobasile/prefect-earthdata/" alt="Stars">
        <img src="https://img.shields.io/github/stars/giorgiobasile/prefect-earthdata?color=0052FF&labelColor=090422" /></a>
    <a href="https://pypistats.org/packages/prefect-earthdata/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/prefect-earthdata?color=0052FF&labelColor=090422" /></a>
    <a href="https://github.com/giorgiobasile/prefect-earthdata/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/giorgiobasile/prefect-earthdata?color=0052FF&labelColor=090422" /></a>
    <br>
    <a href="https://prefect-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>
    <a href="https://discourse.prefect.io/" alt="Discourse">
        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>
</p>

Visit the full docs [here](https://giorgiobasile.github.io/prefect-earthdata) to see additional examples and the API reference.

Prefect integrations with NASA Earthdata, taking advantage of the [`earthaccess`](https://nsidc.github.io/earthaccess/) library.

<a href="https://urs.earthdata.nasa.gov"><img src="https://auth.ops.maap-project.org/cas/images/urs-logo.png" /></a>

## Getting started

`prefect-earthdata` provides a Prefect credentials block and a few tasks to interact with
NASA Earthdata. It does so by leveraging the `earthaccess` library and its API.

Loading the `EarthdataCredentials` block with your credentials, corresponds to calling the [`earthaccess.login()`](https://nsidc.github.io/earthaccess/user-reference/api/api/#earthaccess.api.login) function.

After that, all other `earthaccess` functions can be directly used, without having to login again.

Nevertheless, a few tasks are provided to help taking full advantage of Prefect's observability features.

### Search and download on NASA Earthdata

```python
from prefect import flow, get_run_logger

from prefect_earthdata.credentials import EarthdataCredentials
from prefect_earthdata.tasks import download, search_data


@flow(log_prints=True)
def example_earthdata_download_flow():

    logger = get_run_logger()

    earthdata_credentials = EarthdataCredentials.load("earthdata-credentials")

    granules = search_data(
        earthdata_credentials,
        count=1,
        short_name="ATL08",
        bounding_box=(-92.86, 16.26, -91.58, 16.97),
    )

    logger.info(f"File URL: {granules[0].data_links()[0]}")

    download_path = "/tmp"

    logger.info(f"Downloading data to {download_path}")
    files = download(
        credentials=earthdata_credentials,
        granules=granules,
        local_path=download_path,
    )
    logger.info(f"Downloaded files: {files}")

    return granules, files

example_earthdata_download_flow()
```

Output:

```python
21:07:16.603 | INFO    | prefect.engine - Created flow run 'cheerful-peacock' for flow 'example-earthdata-download-flow'
21:07:18.121 | INFO    | Flow run 'cheerful-peacock' - Created task run 'search_data-0' for task 'search_data'
21:07:18.121 | INFO    | Flow run 'cheerful-peacock' - Executing 'search_data-0' immediately...
21:07:19.642 | INFO    | Task run 'search_data-0' - You're now authenticated with NASA Earthdata Login
21:07:19.644 | INFO    | Task run 'search_data-0' - Using token with expiration date: 09/01/2023
21:07:20.243 | INFO    | Task run 'search_data-0' - Using environment variables for EDL
21:07:21.432 | INFO    | Task run 'search_data-0' - Granules found: 760
21:07:22.211 | INFO    | Task run 'search_data-0' - Finished in state Completed()
21:07:22.225 | INFO    | Flow run 'cheerful-peacock' - File URL: https://data.nsidc.earthdatacloud.nasa.gov/nsidc-cumulus-prod-protected/ATLAS/ATL08/005/2018/11/05/ATL08_20181105083647_05760107_005_01.h5
21:07:22.226 | INFO    | Flow run 'cheerful-peacock' - Downloading data to /tmp
21:07:22.586 | INFO    | Flow run 'cheerful-peacock' - Created task run 'download-0' for task 'download'
21:07:22.587 | INFO    | Flow run 'cheerful-peacock' - Executing 'download-0' immediately...
21:07:24.529 | INFO    | Task run 'download-0' - We are already authenticated with NASA EDL
21:07:28.677 | INFO    | Task run 'download-0' -  Getting 1 granules, approx download size: 0.0 GB
QUEUEING TASKS | : 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 2016.49it/s]
PROCESSING TASKS | : 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:11<00:00, 11.45s/it]
COLLECTING RESULTS | : 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 25115.59it/s]
21:07:40.388 | INFO    | Task run 'download-0' - Finished in state Completed()
21:07:40.392 | INFO    | Flow run 'cheerful-peacock' - Downloaded files: ['ATL08_20181105083647_05760107_005_01.h5']
21:07:41.243 | INFO    | Flow run 'cheerful-peacock' - Finished in state Completed()
```

## Resources

For more tips on how to use tasks and flows in a Collection, check out [Using Collections](https://docs.prefect.io/collections/usage/)!

### Installation

Install `prefect-earthdata` with `pip`:

```bash
pip install prefect-earthdata
```

Requires an installation of Python 3.8+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://docs.prefect.io/).

<!--- ### Saving credentials to block

Note, to use the `load` method on Blocks, you must already have a block document [saved through code](https://docs.prefect.io/concepts/blocks/#saving-blocks) or [saved through the UI](https://docs.prefect.io/ui/blocks/).

Below is a walkthrough on saving block documents through code.

1. Head over to <SERVICE_URL>.
2. Login to your <SERVICE> account.
3. Click "+ Create new secret key".
4. Copy the generated API key.
5. Create a short script, replacing the placeholders (or do so in the UI).

```python
from prefect_earthdata import Block
Block(api_key="API_KEY_PLACEHOLDER").save("BLOCK_NAME_PLACEHOLDER")
```

Congrats! You can now easily load the saved block, which holds your credentials:

```python
from prefect_earthdata import Block
Block.load("BLOCK_NAME_PLACEHOLDER")
```

!!! info "Registering blocks"

    Register blocks in this module to
    [view and edit them](https://docs.prefect.io/ui/blocks/)
    on Prefect Cloud:

    ```bash
    prefect block register -m prefect_earthdata
    ```

A list of available blocks in `prefect-earthdata` and their setup instructions can be found [here](https://giorgiobasile.github.io/prefect-earthdata/blocks_catalog).

--->

### Feedback

If you encounter any bugs while using `prefect-earthdata`, feel free to open an issue in the [prefect-earthdata](https://github.com/giorgiobasile/prefect-earthdata) repository.

If you have any questions or issues while using `prefect-earthdata`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

Feel free to star or watch [`prefect-earthdata`](https://github.com/giorgiobasile/prefect-earthdata) for updates too!

### Contributing

If you'd like to help contribute to fix an issue or add a feature to `prefect-earthdata`, please [propose changes through a pull request from a fork of the repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).

Here are the steps:

1. [Fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo#forking-a-repository)
2. [Clone the forked repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo#cloning-your-forked-repository)
3. Install the repository and its dependencies:
```
pip install -e ".[dev]"
```
4. Make desired changes
5. Add tests
6. Insert an entry to [CHANGELOG.md](https://github.com/giorgiobasile/prefect-earthdata/blob/main/CHANGELOG.md)
7. Install `pre-commit` to perform quality checks prior to commit:
```
pre-commit install
```
8. `git commit`, `git push`, and create a pull request
