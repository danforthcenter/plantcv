import os
from plantcv.plantcv import Objects
from tests import synthetic


def test_save_Objects(tmpdir):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(cache_dir, "test.npz")
    a = Objects([1, 2], [3, 4])
    a.save(outfile)
    assert os.path.exists(outfile)


def test_load_objects(tmp_path):
    """Test for PlantCV."""
    # Save the contour of the plant without the small object to an npz file
    contours, hierarchy = synthetic.find_contours(synthetic.plant_mask(small_object=False))
    outfile = os.path.join(tmp_path, "contours.npz")
    Objects(contours=list(contours), hierarchy=hierarchy).save(outfile)
    obj = Objects.load(outfile)
    # Outline through boundary pixel centers is 236 px long; each of the 4 concave
    # stem-leaf corners is cut by one diagonal step
    assert len(obj.contours[0]) == 232


def test_objects_iteration():
    """Test for PlantCV."""
    obj = Objects([1, 2], [3, 4])
    for i in obj:
        x = i.hierarchy[0]
    assert x == 4
