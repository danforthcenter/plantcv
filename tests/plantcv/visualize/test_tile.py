from plantcv.plantcv.visualize import tile


def test_tile(synthetic_rgb):
    """Test for PlantCV."""
    images = []
    for _ in range(4):
        images.append(synthetic_rgb)
    composite = tile(images=images, ncol=3)
    # Four 100 x 120 images in 3 columns tile into 2 rows: (2 * 100, 3 * 120)
    assert composite.shape == (200, 360, 3)
