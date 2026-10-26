import pytest
import numpy as np
from matplotlib.figure import Figure
from plantcv.plantcv.visualize import pseudocolor
from plantcv.plantcv import params
from tests import synthetic


@pytest.mark.parametrize("debug,axes", [["print", True], ["plot", False], [None, False]])
def test_pseudocolor(debug, axes, tmpdir, synthetic_mask):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    # Input image
    img = synthetic_mask
    r, c = img.shape
    # generate "bad" pixels
    mask_bad = np.zeros((r, c), dtype=np.uint8)
    mask_bad[0:1, 0:1] = 255
    # Debug mode
    params.debug = debug
    pseudo_img = pseudocolor(gray_img=img, mask=None, title="Pseudocolored image", axes=axes, bad_mask=mask_bad)
    # Assert the output is a matplotlib figure
    assert isinstance(pseudo_img, Figure)


@pytest.mark.parametrize("bkgrd,bkgrd_img,axes",
                         [["image", False, True], ["image", True, True], ["white", False, False], ["black", False, True]])
def test_pseudocolor_mask(bkgrd, bkgrd_img, axes, synthetic_mask, synthetic_rgb):
    """Test for PlantCV."""
    # Input image
    img = synthetic_mask
    # Input mask
    mask = synthetic_mask
    r, c = img.shape
    # Input background image
    if bkgrd_img:
        bkgrd = synthetic_rgb

    # generate "bad" pixels
    mask_bad = np.zeros((r, c), dtype=np.uint8)
    mask_bad[0:1, 0:1] = 255
    pseudo_img = pseudocolor(gray_img=img, mask=mask, background=bkgrd, bad_mask=mask_bad,
                             title="Pseudocolored image", axes=axes)
    # Assert the output is a matplotlib figure
    assert isinstance(pseudo_img, Figure)


def test_pseudocolor_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = pseudocolor(gray_img=synthetic_rgb)


def test_pseudocolor_bad_background(synthetic_mask):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = pseudocolor(gray_img=synthetic_mask, mask=synthetic_mask, background="pink")


def test_pseudocolor_bad_background_image_dimensions(synthetic_mask):
    """Test for PlantCV."""
    # 50 x 125 background image that does not match the 100 x 120 input image
    bkgrd = synthetic.plant_rgb(mask=synthetic.two_plants_mask())
    with pytest.raises(RuntimeError):
        _ = pseudocolor(gray_img=synthetic_mask, mask=synthetic_mask, background=bkgrd)
