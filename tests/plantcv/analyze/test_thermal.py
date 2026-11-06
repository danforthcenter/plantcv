from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import thermal as analyze_thermal
from tests import synthetic


def test_thermal():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    img = synthetic.thermal_image()
    mask = synthetic.plant_mask(small_object=False)
    _ = analyze_thermal(thermal_img=img, labeled_mask=mask)
    obs = outputs.observations['default_1']
    # Plant: 240 px at 30 (stem), 280 at 32 (left leaf), 280 at 34 (right leaf)
    assert obs['min_temp']['value'] == 30.0
    assert obs['max_temp']['value'] == 34.0
    # (240 * 30 + 280 * 32 + 280 * 34) / 800 = 32.1
    assert obs['mean_temp']['value'] == 32.1
    # Sorted pixels 400 and 401 are in the left leaf
    assert obs['median_temp']['value'] == 32.0
