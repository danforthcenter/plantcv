import pytest
import numpy as np
from plantcv.plantcv import fill, Objects
from plantcv.plantcv._globals import params
from tests import synthetic


def test_fill(synthetic_mask):
    """Test for PlantCV."""
    # Both objects (plant 800 px, small object 16 px) are smaller than size
    fill_img = fill(bin_img=synthetic_mask, size=1000)
    # Assert the image is blank
    assert np.sum(fill_img) == 0


def test_fill_bad_input(synthetic_gray):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = fill(bin_img=synthetic_gray, size=1)


def test_fill_roi(synthetic_mask):
    """Test for PlantCV."""
    # ROI around the small object only (rows and columns 10:14)
    roi_con = [np.array([[[8, 8]], [[8, 15]], [[15, 15]], [[15, 8]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    fill_img = fill(bin_img=synthetic_mask, size=1000, roi=roi)
    # The small object inside the ROI is removed and the 800 px plant outside it is kept
    assert np.sum(fill_img) == 800 * 255


def test_fill_rescaled(monkeypatch):
    """Test for PlantCV."""
    monkeypatch.setattr(params, "px_height", 0.1)
    monkeypatch.setattr(params, "px_width", 0.1)
    monkeypatch.setattr(params, "unit", "hectares")
    fill_img = fill(bin_img=synthetic.plant_mask(True), size=1, scale_size=True)
    assert np.sum(fill_img / 255) == 800
