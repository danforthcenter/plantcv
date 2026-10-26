import pytest
import numpy as np
from plantcv.plantcv import spatial_clustering
from tests import synthetic


@pytest.mark.parametrize("alg, min_size, max_size", [['DBSCAN', 10, None],
                                                     ['OPTICS', 100, 5000]]
                         )
def test_spatial_clustering(alg, min_size, max_size):
    """Test for PlantCV."""
    img = synthetic.two_plants_mask()
    spmask = spatial_clustering(img, algorithm=alg, min_cluster_size=min_size, max_distance=max_size)
    # Two separate disks
    assert len(spmask[1]) == 2


def test_spatial_clustering_badinput(synthetic_mask):
    """Test for PlantCV."""
    with pytest.raises(NameError):
        _ = spatial_clustering(synthetic_mask, algorithm="Hydra", min_cluster_size=5, max_distance=100)


def test_spatial_clustering_empty_mask():
    """Test for PlantCV."""
    mask = np.zeros((100, 100), dtype=np.uint8)
    spmask = spatial_clustering(mask, algorithm="DBSCAN", min_cluster_size=5, max_distance=100)
    assert spmask[1] == []
