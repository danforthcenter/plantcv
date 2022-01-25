import pytest
import numpy as np
from plantcv.plantcv.visualize import colorize_masks


@pytest.mark.parametrize('colors', [['red', 'blue'], [(0, 0, 255), (255, 0, 0)]])
def test_colorize_masks(colors):
    """Test for PlantCV."""
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    colored_img = colorize_masks(masks=[mask1, mask2], colors=colors)
    # Assert that the output image has the dimensions of the input image
    assert not np.average(colored_img) == 0


def test_colorize_masks_bad_input_empty():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = colorize_masks(masks=[], colors=[])


def test_colorize_masks_bad_input_mismatch_number():
    """Test for PlantCV."""
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    with pytest.raises(RuntimeError):
        _ = colorize_masks(masks=[mask1, mask2], colors=['red', 'green', 'blue'])


def test_colorize_masks_bad_color_input():
    """Test for PlantCV."""
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    with pytest.raises(RuntimeError):
        _ = colorize_masks(masks=[mask1, mask2], colors=['red', 1.123])
