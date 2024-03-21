import cv2
from plantcv.plantcv.transform import merge_images


def test_merge_images_HS(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergehoriz, overlap_percentage=30,
                                 direction="horizontal", method="stacked")
    query_img = cv2.imread(transform_test_data.merged_HS)
    #assert (corrected_img == query_img).all()
    assert corrected_img.shape == query_img.shape


def test_merge_images_HR(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergehoriz, overlap_percentage=30,
                                 direction="horizontal", method="random")
    query_img = cv2.imread(transform_test_data.merged_HS)
    assert corrected_img.shape == query_img.shape


def test_merge_images_HA(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergehoriz, overlap_percentage=30,
                                 direction="horizontal", method="average")
    query_img = cv2.imread(transform_test_data.merged_HA)
    assert (corrected_img == query_img).all()


def test_merge_images_HG(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergehoriz, overlap_percentage=30,
                                 direction="horizontal", method="gradual")
    query_img = cv2.imread(transform_test_data.merged_HG)
    assert (corrected_img == query_img).all()


def test_merge_images_VS(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergevert, overlap_percentage=30,
                                 direction="vertical", method="stacked")
    query_img = cv2.imread(transform_test_data.merged_VS)
    assert (corrected_img == query_img).all()


def test_merge_images_VR(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergevert, overlap_percentage=30,
                                 direction="vertical", method="random")
    query_img = cv2.imread(transform_test_data.merged_VS)
    assert corrected_img.shape == query_img.shape


def test_merge_images_VA(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergevert, overlap_percentage=30,
                                 direction="vertical", method="average")
    query_img = cv2.imread(transform_test_data.merged_VA)
    assert (corrected_img == query_img).all()


def test_merge_images_VG(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergevert, overlap_percentage=30,
                                 direction="vertical", method="gradual")
    query_img = cv2.imread(transform_test_data.merged_VG)
    assert (corrected_img == query_img).all()
