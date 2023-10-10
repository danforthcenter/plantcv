import cv2
from plantcv.plantcv.annotate import ClickCount
from plantcv.plantcv.annotate import clickcount_label


def test_clickcount_label(annotate_test_data):
    """Test for PlantCV."""
    # Read in test data
    img= cv2.imread(annotate_test_data.pollen, -1)
    watershed = cv2.imread(annotate_test_data.pollen_watershed, -1)
    
    totalpoints1=[(158, 531), (361, 112), (500, 418), (269.25303806488864, 385.69839981447126), 
                  (231.21964288863632, 445.995245825603), (293.37177646934134, 448.778177179963), (240.49608073650273, 277.1640769944342), 
                  (279.4571196975417, 240.05832560296852), (77.23077461405376, 165.84682282003712), (420, 364), 
                  (509.5127783246289, 353.2308673469388), (527.1380102355752, 275.3087894248609), (445.50535717435065, 138.94515306122452)]
    germinated1= [(283.3633696975417, 92.56296382189242), (420, 364)]
    counter = ClickCount(img, figsize=(8, 6))
    counter.import_coords(totalpoints1, label="total")
    counter.import_coords(germinated1, label="germinated")

    imagesname = "test"

    _,_,num = clickcount_label(watershed,counter, imagesname)

    assert num == 14

  