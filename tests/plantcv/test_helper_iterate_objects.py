import numpy as np
import pytest
from plantcv.plantcv._helpers import _iterate_objects


def test_iterate_objects_binary_mask(synthetic_mask):
    """Test for PlantCV."""
    mask = synthetic_mask
    objects = list(_iterate_objects(labeled_mask=mask, n_labels=1, label="test"))
    sample, slices, obj_mask = objects[0]
    assert len(objects) == 1
    assert sample == "test_1"
    assert np.count_nonzero(obj_mask) == np.count_nonzero(mask)
    assert obj_mask.shape == mask[slices].shape


def test_iterate_objects_labeled_mask():
    """Test for PlantCV."""
    mask = np.zeros((10, 10), dtype=np.int32)
    mask[1:3, 1:4] = 1
    mask[5:9, 6:8] = 2
    objects = list(_iterate_objects(labeled_mask=mask, n_labels=3, label=["a", "b", "c"]))
    samples = [obj[0] for obj in objects]
    sizes = [np.count_nonzero(obj[2]) for obj in objects]
    assert samples == ["a_1", "b_2", "c_3"]
    assert sizes == [6, 8, 0]


def test_iterate_objects_wrong_num_labels(synthetic_mask):
    """Test for PlantCV."""
    mask = synthetic_mask
    with pytest.raises(RuntimeError):
        _ = list(_iterate_objects(labeled_mask=mask, n_labels=1, label=["test", "test"]))
