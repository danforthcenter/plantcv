import pytest
from plantcv.plantcv import auto_crop
from tests import synthetic


# The plant without the small object has a 60 x 60 bounding box at rows and columns 30:90
@pytest.mark.parametrize('padx,pady,expected', [[10, 10, (80, 80, 3)], [(400, 400), (400, 400), (60, 60, 3)]])
def test_auto_crop(padx, pady, expected, synthetic_rgb):
    """Test for PlantCV."""
    mask = synthetic.plant_mask(small_object=False)
    # Padding that fits in the 100 x 120 image is added; padding that does not is ignored
    cropped = auto_crop(img=synthetic_rgb, mask=mask, padding_x=padx, padding_y=pady, color='image')
    assert cropped.shape == expected


@pytest.mark.parametrize("color", ["black", "white", "image"])
def test_auto_crop_grayscale(color, synthetic_gray):
    """Test for PlantCV."""
    mask = synthetic.plant_mask(small_object=False)
    cropped = auto_crop(img=synthetic_gray, mask=mask, padding_x=10, padding_y=10, color=color)
    # 60 x 60 bounding box plus 10 px of padding on each side
    assert cropped.shape == (80, 80)


def test_auto_crop_bad_color_input(synthetic_gray):
    """Test for PlantCV."""
    mask = synthetic.plant_mask(small_object=False)
    with pytest.raises(RuntimeError):
        _ = auto_crop(img=synthetic_gray, mask=mask, padding_x=10, padding_y=10, color='wite')


def test_auto_crop_bad_padding_input(synthetic_gray):
    """Test for PlantCV."""
    mask = synthetic.plant_mask(small_object=False)
    with pytest.raises(RuntimeError):
        _ = auto_crop(img=synthetic_gray, mask=mask, padding_x="one", padding_y=10, color='white')
