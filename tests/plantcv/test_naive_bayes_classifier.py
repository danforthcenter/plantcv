import pytest
import numpy as np
from plantcv.plantcv import naive_bayes_classifier
from tests import synthetic


def test_naive_bayes_classifier(synthetic_rgb, synthetic_mask, tmp_path):
    """Test for PlantCV."""
    masks = naive_bayes_classifier(rgb_img=synthetic_rgb, pdf_file=synthetic.write_nb_pdfs(tmp_path))
    assert list(masks) == ["plant", "background"]
    # The plant (HSV 60, 255, 128) is at the peak of every plant PDF, and the background (HSV 0, 0, 128) at
    # the peak of every background PDF; their hues are 6 standard deviations (60 / 10) from the other class's
    assert np.array_equal(masks["plant"], synthetic_mask)
    assert np.array_equal(masks["background"], 255 - synthetic_mask)


def test_naive_bayes_classifier_bad_input(synthetic_rgb, tmp_path):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = naive_bayes_classifier(rgb_img=synthetic_rgb, pdf_file=synthetic.write_nb_pdfs(tmp_path, bad=True))
