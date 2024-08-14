import plantcv.plantcv as pcv
import cv2
from plantcv.plantcv.visualize import tile


def test_tile(visualize_test_data):
    """Test for PlantCV."""
    # Read in image list
    images = []
    paths = [visualize_test_data.tile_dir+"Tile_1.jpg", visualize_test_data.tile_dir+"Tile_2.jpg",
             visualize_test_data.tile_dir+"Tile_3.jpg", visualize_test_data.tile_dir+"Tile_4.jpg"]
    for i in paths:
        images.append(pcv.readimage(i)[0])
    composite = tile(images=images, nrow=2, ncol=3)
    query_img = cv2.imread(visualize_test_data.tile_out)
    assert (composite == query_img).all()