import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_width


def test_segment_width(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    mask = cv2.imread(test_data.labeled_mask, -1)
    skeleton = cv2.imread(test_data.small_bin_fill, -1)
    _ = segment_width(img=skeleton, labeled_mask=mask)
    assert int(sum(outputs.observations['default']['segment_width']['value'])) == 12

