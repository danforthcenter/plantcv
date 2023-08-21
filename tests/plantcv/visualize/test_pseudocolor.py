import pytest
import cv2
import numpy as np
from matplotlib.figure import Figure
from plantcv.plantcv.visualize import pseudocolor
from plantcv.plantcv import params


@pytest.mark.parametrize("debug,axes", [["print", True], ["plot", False], [None, False]])
def test_pseudocolor(debug, axes, tmpdir, visualize_test_data):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Input image
    img = cv2.imread(visualize_test_data.small_bin_img, -1)
    r, c = img.shape
    # generate "bad" pixels
    mask_bad = np.zeros((r, c), dtype=np.uint8)
    mask_bad[0:1, 0:1] = 255
    # Debug mode
    params.debug = debug
    pseudo_img = pseudocolor(gray_img=img, mask=None, title="Pseudocolored image", axes=axes, bad_mask=mask_bad)
    # Assert the output is a matplotlib figure
    assert isinstance(pseudo_img, Figure)


@pytest.mark.parametrize("bkgrd,axes", [["image", True], ["white", False], ["black", True]])
def test_pseudocolor_mask(bkgrd, axes, visualize_test_data):
    """Test for PlantCV."""
    # Input image
    img = cv2.imread(visualize_test_data.small_bin_img, -1)
    # Input mask
    mask = cv2.imread(visualize_test_data.small_bin_img, -1)
    r, c = img.shape
    # generate "bad" pixels
    mask_bad = np.zeros((r, c), dtype=np.uint8)
    mask_bad[0:1, 0:1] = 255
    pseudo_img = pseudocolor(gray_img=img, mask=mask, background=bkgrd, bad_mask=mask_bad,
                             title="Pseudocolored image", axes=axes)
    # Assert the output is a matplotlib figure
    assert isinstance(pseudo_img, Figure)


def test_pseudocolor_bad_input(visualize_test_data):
    """Test for PlantCV."""
    img = cv2.imread(visualize_test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = pseudocolor(gray_img=img)


def test_pseudocolor_bad_background(visualize_test_data):
    """Test for PlantCV."""
    img = cv2.imread(visualize_test_data.small_bin_img, -1)
    mask = cv2.imread(visualize_test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        _ = pseudocolor(gray_img=img, mask=mask, background="pink")
