from plantcv.plantcv import rgb2gray


def test_rgb2gray(synthetic_rgb):
    """Test for PlantCV."""
    gray_img = rgb2gray(rgb_img=synthetic_rgb)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert synthetic_rgb.shape[:2] == gray_img.shape
