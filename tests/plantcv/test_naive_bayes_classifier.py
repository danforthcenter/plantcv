import pytest
import numpy as np
from plantcv.plantcv import naive_bayes_classifier
from tests import synthetic


def test_naive_bayes_classifier(test_data):
    """Test for PlantCV."""
    # The trained PDFs favor plant at hue 34-49, so color the plant BGR (40, 133, 102) (HSV 40, 178, 133)
    mask = synthetic.plant_mask()
    img = synthetic.plant_rgb(mask=mask)
    img[mask > 0] = (40, 133, 102)
    masks = naive_bayes_classifier(rgb_img=img, pdf_file=test_data.nb_trained_model)
    # Assert that the output image has the dimensions of the input image
    results = [len(masks) == 2]
    for mask_img in masks.values():
        results.append(np.array_equal(np.unique(mask_img), np.array([0, 255])))
    assert all(results)
    # Plant pixels are classified as plant and gray background (saturation 0) as background
    assert np.array_equal(masks["plant"], mask)
    assert np.array_equal(masks["background"], 255 - mask)


def test_naive_bayes_classifier_bad_input(test_data, synthetic_rgb):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = naive_bayes_classifier(rgb_img=synthetic_rgb, pdf_file=test_data.nb_bad_model)
