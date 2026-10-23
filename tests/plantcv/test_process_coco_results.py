import os
import numpy as np
from plantcv.plantcv.classes import COCO
from plantcv.plantcv.process_coco_results import process_coco_results


def test_process_coco_results(tmpdir):
    """Test for PlantCV."""
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[30:70, 30:70] = 1
    mask2 = np.zeros((150, 150), dtype=np.uint8)
    mask2[30:70, 30:70] = 1
    coco1 = COCO(mask)
    coco2 = COCO(mask2)
    cache_dir = tmpdir.mkdir("cache")
    outpath1 = os.path.join(cache_dir, "coco1.json")
    outpath2 = os.path.join(cache_dir, "coco2.json")
    coco1.save(outpath1)
    coco2.save(outpath2)
    outpath3 = os.path.join(cache_dir, "combined.json")
    process_coco_results(filename=outpath3, source=str(cache_dir), pattern=None)
    assert os.path.exists(outpath3)
    coco3 = COCO()
    coco3.load(outpath3)
    assert len(coco3.annotations) == 2

