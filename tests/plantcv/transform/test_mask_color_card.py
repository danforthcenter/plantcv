"""Tests for filters.color_card."""
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.transform.detect_color_card import mask_color_card
from tests import synthetic


def test_mask_color_card():
    """Test for PlantCV."""
    params.debug = "plot"
    rgb_img = synthetic.color_card()
    cc_mask = mask_color_card(rgb_img=rgb_img)
    assert np.array_equal(np.unique(cc_mask), np.array([0, 255]))
    # The bounding box covers every chip and stays on the card body
    m = synthetic.COLOR_CARD_MARGIN
    assert np.all(cc_mask[synthetic.color_card_mask() > 0] == 255)
    body = np.zeros(synthetic.COLOR_CARD_SHAPE, dtype=bool)
    body[m:-m, m:-m] = True
    assert not np.any(cc_mask[~body])


def test_mask_astro_color_card():
    """Test for PlantCV."""
    params.debug = "plot"
    rgb_img = synthetic.astro_card()
    cc_mask = mask_color_card(rgb_img=rgb_img, card_type="astro")
    # The tags are at their reference positions scaled by 0.4, so the 600 x 700 reference card maps onto the
    # 240 x 280 card body at rows and columns 30 onward
    m = synthetic.ASTRO_CARD_MARGIN
    expected = np.zeros(synthetic.ASTRO_CARD_SHAPE, dtype=np.uint8)
    expected[m:-m, m:-m] = 255
    assert np.array_equal(cc_mask, expected)
