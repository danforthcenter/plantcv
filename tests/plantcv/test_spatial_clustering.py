import pytest
import cv2
from plantcv.plantcv import spatial_clustering


@pytest.mark.parametrize("alg, min_size, max_size", [['DBSCAN', 10, None],
                                                     ['OPTICS', 100, 5000]]
                         )
def test_spatial_clustering(alg, min_size, max_size, test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.multi_bin_img, -1)
    spmask = spatial_clustering(img, algorithm=alg, min_cluster_size=min_size, max_distance=max_size)
    assert len(spmask[1]) == 2


def test_spatial_clustering_badinput(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_bin_img)
    with pytest.raises(NameError):
        _ = spatial_clustering(img, algorithm="Hydra", min_cluster_size=5, max_distance=100)
