import pytest
from plantcv.plantcv.io import random_subset


def test_random_subset():
    """Test for PlantCV."""
    full_list = ['a', 'b', 'c', 'd', 'e']
    n_samples = 3
    samples_list = random_subset(dataset=full_list, num=n_samples, seed=None)
    assert set(samples_list).issubset(set(full_list))


def test_random_subset_greater_than_len():
    """Test for PlantCV."""
    full_list = ['a', 'b', 'c', 'd', 'e']
    # test error when asking for one more sample than the existent number in the list
    n_samples = len(full_list) + 1
    with pytest.raises(RuntimeError):
        _ = random_subset(dataset=full_list, num=n_samples, seed=None)
