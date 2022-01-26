import os
from plantcv.plantcv import print_results


def test_print_results(tmpdir):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(cache_dir, "results.json")
    print_results(filename=outfile)
    assert os.path.exists(outfile)
