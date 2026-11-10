import os
import random
import pytest
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.submask import sub_mask
from tests import synthetic

random.seed(a=123)


def test_sub_mask_success(synthetic_rgb, synthetic_mask, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    debug_state = params.debug
    params.debug = "print"
    params.debug_outdir = str(cache_dir)
    spots = sub_mask(synthetic_rgb, synthetic_mask, 2, 2)
    params.debug = debug_state
    # Background plus two labeled radius-2 circles, which fit in the 10 px thick leaves
    assert len(np.unique(spots)) == 3
    assert len(os.listdir(cache_dir)) == 1


def test_sub_mask_too_large(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    spots = sub_mask(synthetic_rgb, synthetic_mask, 2, 20)
    # A radius-20 circle does not fit anywhere in the plant, so only background remains
    assert len(np.unique(spots)) == 1


def test_sub_mask_too_many():
    """Test for PlantCV."""
    # A radius-3 circle fits in a radius-4 disk only near its center, so just one of five can be placed
    mask = synthetic.disk_mask(synthetic.PLANT_SHAPE, [(50, 60)], 4)
    img = synthetic.plant_rgb(mask=mask)
    spots = sub_mask(img, mask, 5, 3)
    # Background plus one circle (relabeled 255)
    assert len(np.unique(spots)) == 2


def test_sub_mask_empty(synthetic_rgb):
    """Test for PlantCV."""
    mask = np.zeros(synthetic_rgb.shape[0:2])
    with pytest.raises(RuntimeError):
        _ = sub_mask(synthetic_rgb, mask, 5, 3)
