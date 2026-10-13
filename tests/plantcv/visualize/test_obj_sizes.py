import pytest
import cv2
import numpy as np
from plantcv.plantcv.visualize import obj_sizes
from plantcv.plantcv._globals import params


@pytest.mark.parametrize("num,expected", [[100, 4], [1, 4]])
def test_obj_sizes(num, expected, test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.multi_bin_img, -1)
    visualization = obj_sizes(img=img, mask=img, num_objects=num)
    # Output unique colors are the 32 objects, the gray text, the black background, and white unlabeled leaves
    assert len(np.unique(visualization.reshape(-1, visualization.shape[2]), axis=0)) == expected


def test_obj_sizes_rescaled(test_data):
    """Test for PlantCV."""
    prev_px_height = params.px_height
    prev_px_width = params.px_width
    params.px_height = 0.1
    params.px_width = 0.1
    params.unit = "hectares"
    img = np.zeros((100, 100), dtype=np.uint8)
    img[0:10, 0:10] = 1
    img[11:40, 11:40] = 1
    img[50:99, 50:99] = 1
    x1 = obj_sizes(img, img, 100, scale_size=False)
    x2 = obj_sizes(img, img, 100, scale_size=True)
    params.px_height = prev_px_height
    params.px_width = prev_px_width
    params.unit = "pixels"
    assert np.sum(x1) != np.sum(x2)
