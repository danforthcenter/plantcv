from plantcv.plantcv.morphology.segment_id import segment_id
from tests import synthetic


def test_segment_id():
    """Test for PlantCV."""
    skel = synthetic.skeleton()
    leaf_obj, _ = synthetic.skeleton_segments()
    _, labeled_img = segment_id(skel_img=skel, objects=leaf_obj, mask=skel)
    assert skel.shape == labeled_img.shape[:2]


def test_segment_id_no_mask():
    """Test for PlantCV."""
    skel = synthetic.skeleton()
    leaf_obj, _ = synthetic.skeleton_segments()
    _, labeled_img = segment_id(skel_img=skel, objects=leaf_obj)
    assert skel.shape == labeled_img.shape[:2]
