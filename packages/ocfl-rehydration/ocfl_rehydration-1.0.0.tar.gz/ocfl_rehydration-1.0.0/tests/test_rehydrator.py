import os
import shutil
import pytest
from project_paths import paths
from ocfl_rehydration.rehydrator import Rehydrator

@pytest.fixture
def batch_name():
    return "1028626.xml"

@pytest.fixture
def output_dir():
    return os.path.join(paths.dir_unit_out, 'rehydrator_test')

@pytest.fixture
def rehydrator(output_dir):
    ocfl_object_path = os.path.join(paths.dir_unit_resources, 'data/27340448')
    return Rehydrator(ocfl_object_path, output_dir)

@pytest.fixture
def expected_files():
    return [
        "_002635021_0001.tif",
        "_002635021_0001.txt",
        "_002635021_0002.tif",
        "_002635021_0002.txt",
        "_002635021_0003.tif",
        "_002635021_0003.txt",
        "_002635021_0004.tif",
        "_002635021_0004.txt",
        "_002635021_0005.tif",
        "_002635021_0005.txt",
        "_002635021_0006.tif",
        "_002635021_0006.txt"
    ]


def test_rehydrate(rehydrator, expected_files, output_dir, batch_name):
    rehydrator.rehydrate()

    for expected_file in expected_files:
        assert os.path.exists(os.path.join(output_dir, batch_name, expected_file))

    shutil.rmtree(output_dir)