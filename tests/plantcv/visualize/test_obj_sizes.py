import pytest
import numpy as np
from plantcv.plantcv.visualize import obj_sizes
from plantcv.plantcv._globals import params
from tests import synthetic


@pytest.mark.parametrize("num,expected", [[100, 4], [1, 4]])
def test_obj_sizes(num, expected):
    """Test for PlantCV."""
    img = synthetic.two_plants_mask()
    visualization = obj_sizes(img=img, mask=img, num_objects=num)
    # With num=100 the unique colors are the 2 objects, the gray text, and the black background;
    # with num=1 they are 1 object, the gray text, the black background, and the white unlabeled plant
    assert len(np.unique(visualization.reshape(-1, visualization.shape[2]), axis=0)) == expected


def test_obj_sizes_rescaled(monkeypatch):
    """Test for PlantCV."""
    monkeypatch.setattr(params, "px_height", 0.1)
    monkeypatch.setattr(params, "px_width", 0.1)
    monkeypatch.setattr(params, "unit", "hectares")
    img = synthetic.plant_mask(True)
    x1 = obj_sizes(img, img, 100, scale_size=False)
    x2 = obj_sizes(img, img, 100, scale_size=True)
    assert np.sum(x1) != np.sum(x2)
