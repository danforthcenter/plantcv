import cv2
from plantcv.plantcv.transform import merge_images

def test_merge_images_HS(test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(test_data.mergehoriz, overlap_percentage = 30,
                                 direction = "horizontal", method = "stacked")
    query_img = cv2.imread(test_data.merged_HS)
    assert corrected_img == query_img
    
def test_merge_images_HR(test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(test_data.mergehoriz, overlap_percentage = 30,
                                 direction = "horizontal", method = "random")
    query_img = cv2.imread(test_data.merged_HS)
    assert corrected_img.shape == query_img.shape
    
def test_merge_images_HA(test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(test_data.mergehoriz, overlap_percentage = 30,
                                 direction = "horizontal", method = "average")
    query_img = cv2.imread(test_data.merged_HA)
    assert corrected_img == query_img
    
def test_merge_images_HG(test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(test_data.mergehoriz, overlap_percentage = 30,
                                 direction = "horizontal", method = "gradual")
    query_img = cv2.imread(test_data.merged_HG)
    assert corrected_img == query_img
    
def test_merge_images_VS(test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(test_data.mergevert, overlap_percentage = 30,
                                 direction = "vertical", method = "stacked")
    query_img = cv2.imread(test_data.merged_VS)
    assert corrected_img == query_img
    
def test_merge_images_VR(test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(test_data.mergevert, overlap_percentage = 30,
                                 direction = "vertical", method = "random")
    query_img = cv2.imread(test_data.merged_VS)
    assert corrected_img.shape == query_img.shape
    
def test_merge_images_VA(test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(test_data.mergevert, overlap_percentage = 30,
                                 direction = "vertical", method = "average")
    query_img = cv2.imread(test_data.merged_VA)
    assert corrected_img == query_img
    
def test_merge_images_VG(test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(test_data.mergevert, overlap_percentage = 30,
                                 direction = "vertical", method = "gradual")
    query_img = cv2.imread(test_data.merged_VG)
    assert corrected_img == query_img
    