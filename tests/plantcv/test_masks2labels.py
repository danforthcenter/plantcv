from plantcv.plantcv import masks2labels
import pickle


def test_masks2labels(test_data):
    """Test for PlantCV."""
    with open(test_data.masks_list, "rb") as f:
        masks_list = pickle.load(f)

    _, _, num_label = masks2labels(masks_list)

    assert num_label == 33
