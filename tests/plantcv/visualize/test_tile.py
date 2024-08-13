import os
import plantcv.plantcv as pcv
from plantcv.plantcv.visualize import tile


def test_tile(visualize_test_data):
    """Test for PlantCV."""
    # Read in image list
    images = []
    paths = [visualize_test_data.tile_dir+"Tile1.png", visualize_test_data.tile_dir+"Tile2.png",
             visualize_test_data.tile_dir+"Tile3.png", visualize_test_data.tile_dir+"Tile4.png"]
    #paths = [visualize_test_data.tile_dir+i for i in os.listdir(visualize_test_data.tile_dir)]
    paths.sort
    for i in paths:
        images.append(pcv.readimage(i)[0])
    composite = tile(images=images, nrow=2, ncol=3)
    query_img, _, _ = pcv.readimage(visualize_test_data.tile_out)
    assert (composite == query_img).all()