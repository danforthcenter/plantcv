import os
from plantcv.plantcv import Objects


def test_save_Objects(tmpdir):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(cache_dir, "test.npz")
    a = Objects([1, 2], [3, 4])
    a.save(outfile)
    assert os.path.exists(outfile)


def test_load_objects(test_data):
    """Test for PlantCV."""
    # Load in npz file
    obj = Objects.load(test_data.small_contours_file)
    assert len(obj.contours[0]) == 130


def test_objects_iteration():
    """Test for PlantCV."""
    obj = Objects([1, 2], [3, 4])
    for i in obj:
        x = i.hierarchy[0]
    assert x == 4
