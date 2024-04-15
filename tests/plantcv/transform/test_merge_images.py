import cv2
import os
import plantcv.plantcv as pcv
from plantcv.plantcv.transform import merge_images


def test_merge_images_HS(transform_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    corrected_img = merge_images(transform_test_data.mergehoriz, overlap_percentage=30,
                                 direction="horizontal", method="stacked")
    pcv.print_image(corrected_img, os.path.join(cache_dir, "merged_img.jpg"))
    merged_img = cv2.imread(os.path.join(cache_dir, "merged_img.jpg"))
    query_img = cv2.imread(transform_test_data.merged_HS)
    assert (merged_img == query_img).all()


def test_merge_images_HR(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergehoriz, overlap_percentage=30,
                                 direction="horizontal", method="random")
    query_img = cv2.imread(transform_test_data.merged_HS)
    assert corrected_img.shape == query_img.shape


def test_merge_images_HA(transform_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    corrected_img = merge_images(transform_test_data.mergehoriz, overlap_percentage=30,
                                 direction="horizontal", method="average")
    pcv.print_image(corrected_img, os.path.join(cache_dir, "merged_img.jpg"))
    merged_img = cv2.imread(os.path.join(cache_dir, "merged_img.jpg"))
    query_img = cv2.imread(transform_test_data.merged_HA)
    assert (merged_img == query_img).all()


def test_merge_images_HG(transform_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    corrected_img = merge_images(transform_test_data.mergehoriz, overlap_percentage=30,
                                 direction="horizontal", method="gradual")
    pcv.print_image(corrected_img, os.path.join(cache_dir, "merged_img.jpg"))
    merged_img = cv2.imread(os.path.join(cache_dir, "merged_img.jpg"))
    query_img = cv2.imread(transform_test_data.merged_HG)
    assert (merged_img == query_img).all()


def test_merge_images_VS(transform_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    corrected_img = merge_images(transform_test_data.mergevert, overlap_percentage=30,
                                 direction="vertical", method="stacked")
    pcv.print_image(corrected_img, os.path.join(cache_dir, "merged_img.jpg"))
    merged_img = cv2.imread(os.path.join(cache_dir, "merged_img.jpg"))
    query_img = cv2.imread(transform_test_data.merged_VS)
    assert (merged_img == query_img).all()


def test_merge_images_VR(transform_test_data):
    """Test for PlantCV."""
    corrected_img = merge_images(transform_test_data.mergevert, overlap_percentage=30,
                                 direction="vertical", method="random")
    query_img = cv2.imread(transform_test_data.merged_VS)
    assert corrected_img.shape == query_img.shape


def test_merge_images_VA(transform_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    corrected_img = merge_images(transform_test_data.mergevert, overlap_percentage=30,
                                 direction="vertical", method="average")
    pcv.print_image(corrected_img, os.path.join(cache_dir, "merged_img.jpg"))
    merged_img = cv2.imread(os.path.join(cache_dir, "merged_img.jpg"))
    query_img = cv2.imread(transform_test_data.merged_VA)
    assert (merged_img == query_img).all()


def test_merge_images_VG(transform_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    corrected_img = merge_images(transform_test_data.mergevert, overlap_percentage=30,
                                 direction="vertical", method="gradual")
    pcv.print_image(corrected_img, os.path.join(cache_dir, "merged_img.jpg"))
    merged_img = cv2.imread(os.path.join(cache_dir, "merged_img.jpg"))
    query_img = cv2.imread(transform_test_data.merged_VG)
    assert (merged_img == query_img).all()
