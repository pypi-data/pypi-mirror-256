from osdata import Datasets

ds = Datasets()


def test_ds_list():
    assert ds.list() == "Listing all your available datasets"


def test_ds_get():
    assert ds.get(id="123") == 'Retreiving dataset with ID: {id}'
