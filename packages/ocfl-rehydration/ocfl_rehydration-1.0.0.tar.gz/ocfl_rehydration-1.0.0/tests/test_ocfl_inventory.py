import os
import pytest
from project_paths import paths
from ocfl_rehydration.ocfl_inventory import OcflInventory


@pytest.fixture
def inventory_file():
    inventory_json = 'data/16952962/v00001/inventory.json'
    return os.path.join(paths.dir_unit_resources, inventory_json)


def test_get_descriptor_path(inventory_file):
    inventory = OcflInventory(open(inventory_file))
    descriptor_path = inventory.get_descriptor_path()
    assert descriptor_path == 'v00001/content/descriptor/46296439_mets.xml'


def test_get_data_path(inventory_file):
    inventory = OcflInventory(open(inventory_file))
    data_path = inventory.get_data_path('46296441')
    assert data_path == 'v00001/content/data/46296441.txt'