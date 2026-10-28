from plantcv.plantcv._helpers import _grayscale_to_rgb


def test_grayscale_to_rgb(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    img = _grayscale_to_rgb(img=img)
    assert len(img.shape) == 3
