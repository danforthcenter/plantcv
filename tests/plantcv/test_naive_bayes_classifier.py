import pytest
import cv2
import numpy as np
from plantcv.plantcv import naive_bayes_classifier


def test_naive_bayes_classifier(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    masks = naive_bayes_classifier(rgb_img=img, pdf_file=test_data.nb_trained_model)
    # Assert that the output image has the dimensions of the input image
    results = [len(masks) == 2]
    for mask in masks.values():
        results.append(np.array_equal(np.unique(mask), np.array([0, 255])))
    assert all(results)


def test_naive_bayes_classifier_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = naive_bayes_classifier(rgb_img=img, pdf_file=test_data.nb_bad_model)
