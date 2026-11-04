import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology.fill_segments import fill_segments
from tests import synthetic


def test_fill_segments():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = synthetic.skeleton_mask()
    leaves, stem = synthetic.skeleton_segments()
    _ = fill_segments(mask=mask, objects=leaves, stem_objects=stem)
    leaf_area = outputs.observations['default']["leaf_area"]["value"]
    stem_area = outputs.observations['default']["stem_area"]["value"]
    assert leaf_area == [81, 83, 98, 101]  # recorded value
    assert stem_area == 153  # recorded value
    # Every mask pixel is assigned to a segment
    assert sum(leaf_area) + stem_area == np.count_nonzero(mask)
    assert outputs.observations['default']["stem_area"]["scale"] == "pixels"


def test_fill_segments_no_stem():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = synthetic.skeleton_mask()
    leaves, stem = synthetic.skeleton_segments()
    _ = fill_segments(mask=mask, objects=stem + leaves)
    segment_area = outputs.observations['default']['segment_area']['value']
    assert segment_area == [56, 25, 32, 98, 100, 100, 105]  # recorded value
    # Every mask pixel is assigned to a segment
    assert sum(segment_area) == np.count_nonzero(mask)
    assert outputs.observations['default']['segment_area']['scale'] == "pixels"
