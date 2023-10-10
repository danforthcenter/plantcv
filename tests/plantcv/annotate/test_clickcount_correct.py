import cv2
import numpy as np
from plantcv.plantcv.annotate import ClickCount
from plantcv.plantcv.annotate import clickcount_correct


def test_plantcv_click_count_correct(annotate_test_data):
    """Test for PlantCV."""
    # Create a test tmp directory
    # generate fake testing image
    img= cv2.imread(annotate_test_data.pollen, -1)
    allmask = cv2.imread(annotate_test_data.pollen_all, -1)
    discs = cv2.imread(annotate_test_data.pollen_discs, -1)
    
    coor=[(158, 531), (265, 427), (361, 112), (500, 418)]
    totalpoints1=[(158, 531), (361, 112), (500, 418), (269.25303806488864, 385.69839981447126), 
                  (231.21964288863632, 445.995245825603), (293.37177646934134, 448.778177179963), (240.49608073650273, 277.1640769944342), 
                  (279.4571196975417, 240.05832560296852), (77.23077461405376, 165.84682282003712), (423.24190633947126, 364.3625927643785), 
                  (509.5127783246289, 353.2308673469388), (527, 275), (445.50535717435065, 138.94515306122452)]
    germinated1= [(283.3633696975417, 92.56296382189242), (429.93108769383116, 369.0008116883117)]
    counter = ClickCount(img, figsize=(8, 6))
    counter.import_coords(totalpoints1, label="total")
    counter.import_coords(germinated1, label="germinated")

    corrected_mask, _ = clickcount_correct(discs,allmask, counter, coor)

    assert np.count_nonzero(discs)< np.count_nonzero(corrected_mask) 
    assert np.count_nonzero(corrected_mask) < np.count_nonzero(allmask)