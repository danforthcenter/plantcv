import pytest
import cv2
import numpy as np
from plantcv.plantcv import crop_position_mask


@pytest.mark.parametrize("v_pos,h_pos", [["top", "right"], ["bottom", "left"]])
def test_crop_position_mask(v_pos, h_pos, test_data, synthetic_mask):
    """Test for PlantCV."""
    # Read in test data - img is bigger than mask and both are grayscale
    img = cv2.imread(test_data.fmax, -1)
    newmask = crop_position_mask(img=img, mask=synthetic_mask, x=40, y=3, v_pos=v_pos, h_pos=h_pos)
    assert newmask.shape == img.shape


def test_crop_position_rgb_inputs(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    newmask = crop_position_mask(img=img, mask=synthetic_mask, x=40, y=3, v_pos="top", h_pos="left")
    assert newmask.shape == img.shape[:2]


# A mask 51 rows shorter than the 100 row image, moved down x - 1 = 39 rows, needs an even
# number (12) of padding rows
@pytest.mark.parametrize("v_pos,h_pos,r,c", [
    ["top", "right", 51, 49],
    ["bottom", "left", 51, 49],
    ["top", "right", -51, -49],
    ["bottom", "left", -51, -49]
    ])
def test_crop_position_mask_size(v_pos, h_pos, r, c, synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    h, w = img.shape
    mask = np.zeros((h + r, w + c), dtype=np.uint8)
    newmask = crop_position_mask(img=img, mask=mask, x=40, y=3, v_pos=v_pos, h_pos=h_pos)
    assert newmask.shape == img.shape


@pytest.mark.parametrize("x,y,v_pos,h_pos", [
    [-1, -1, "top", "right"],  # Invalid x and y
    [40, 3, "below", "right"],  # Invalid v_pos
    [40, 3, "top", "starboard"],  # Invalid h_pos
    [40, 3, "top", "left"]  # Invalid dtype of mask
    ])
def test_crop_position_mask_bad_inputs(x, y, v_pos, h_pos, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.fmax, -1)
    mask = cv2.imread(test_data.fmax, -1)
    with pytest.raises(RuntimeError):
        _ = crop_position_mask(img=img, mask=mask, x=x, y=y, v_pos=v_pos, h_pos=h_pos)
