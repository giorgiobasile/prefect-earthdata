from pathlib import Path
from tempfile import TemporaryDirectory

from prefect import flow
from prefect.testing.utilities import prefect_test_harness

from prefect_earthdata.tasks import download, search_data


def test_search_data_and_download(earthdata_credentials_mock):  # noqa
    @flow
    def test_flow(download_path):
        granules = search_data(
            earthdata_credentials_mock,
            count=1,
            short_name="ATL08",
            bounding_box=(-92.86, 16.26, -91.58, 16.97),
        )
        files = download(earthdata_credentials_mock, granules, download_path)

        return granules, files

    with TemporaryDirectory() as temp_dir:
        with prefect_test_harness():
            granules, files = test_flow(temp_dir)
            assert isinstance(granules, list)
            assert len(granules) == 1
            assert files == ["ATL08_20181105083647_05760107_005_01.h5"]
            assert Path(temp_dir, "ATL08_20181105083647_05760107_005_01.h5").exists()
