import numpy as np
from plantcv.plantcv import floodfill, Objects


def test_floodfill(synthetic_mask):
    """Test for PlantCV."""
    # One seed point (x, y) in the plant stem and one in the small object
    fill_img = floodfill(bin_img=synthetic_mask, points=[(60, 60), (12, 12)], value=0)
    # Assert that the image has been filled in
    assert np.sum(fill_img) == 0


def test_floodfill_roi(synthetic_mask):
    """Test for PlantCV."""
    # ROI between the small object and the plant, containing no foreground
    roi_con = [np.array([[[10, 20]], [[10, 29]], [[29, 29]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    fill_img = floodfill(bin_img=synthetic_mask, points=[(1, 1), (5, 5), (8, 8)], value=0, roi=roi)
    # Assert that the image has not been filled in: plant 800 px plus small object 16 px
    assert np.sum(fill_img) == 816 * 255
