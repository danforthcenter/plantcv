import plantcv.plantcv as pcv
from plantcv.plantcv.visualize import tile


def test_tile(visualize_test_data):
    """Test for PlantCV."""
    # Read in image list
    images = []
    paths = [visualize_test_data.tile_dir+"Tile_1.jpg", visualize_test_data.tile_dir+"Tile_2.jpg",
             visualize_test_data.tile_dir+"Tile_3.jpg", visualize_test_data.tile_dir+"Tile_4.jpg"]
    for i in paths:
        images.append(pcv.readimage(i)[0])
    composite = tile(images=images, ncol=3)
    assert composite.shape == (663, 855, 3)