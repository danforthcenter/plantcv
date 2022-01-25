import numpy as np
from plantcv.plantcv.visualize import colorize_label_img


def test_colorize_label_img():
    """Test for PlantCV."""
    label_img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    colored_img = colorize_label_img(label_img)
    assert (colored_img.shape[0:-1] == label_img.shape) and colored_img.shape[-1] == 3
