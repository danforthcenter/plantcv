import os
import cv2
from plantcv.plantcv import output_mask


def test_output_mask(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    imgpath, maskpath, _ = output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir, mask_only=False)
    assert all([os.path.exists(imgpath) is True, os.path.exists(maskpath) is True])
