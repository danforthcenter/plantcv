import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_width


def test_segment_width():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Label 1 is a 7-pixel-tall bar (rows 40:47) with its midline (row 43) as the skeleton,
    # away from the bar ends. Label 2 is a single pixel off the skeleton.
    labeled_mask = np.zeros((100, 100), dtype=np.int32)
    labeled_mask[40:47, 10:90] = 1
    labeled_mask[80, 80] = 2
    skeleton = np.zeros((100, 100), dtype=np.uint8)
    skeleton[43, 30:70] = 255
    _ = segment_width(segmented_img=labeled_mask.astype(np.uint8), skel_img=skeleton,
                      labeled_mask=labeled_mask, n_labels=2)
    # The dilated midline covers rows 42 and 43 equally, at distances 3 and 4 from the background:
    # mean width 2 * 3.5 = 7, the bar height
    assert outputs.observations['default']['mean_segment_width']['value'] == [7, 0]
    assert outputs.observations['default']['segment_width_max']['value'] == [8, 0]
    assert outputs.observations['default']['segment_width_std']['value'] == [0.5, "NA"]
