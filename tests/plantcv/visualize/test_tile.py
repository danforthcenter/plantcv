import os
import plantcv.plantcv as pcv
from plantcv.plantcv.visualize import tile


def test_tile(visualize_test_data):
    """Test for PlantCV."""
    pcv.params.debug = "plot"
    # Read in image list
    images = []
    for i in os.listdir(visualize_test_data.tile_dir):
        images.append(pcv.readimage(visualize_test_data.tile_dir+i)[0])
    images.sort
    composite = tile(images=images, nrow=2, ncol=3)
    query_img, _, _ = pcv.readimage(visualize_test_data.tile_out)
    assert (composite == query_img).all()