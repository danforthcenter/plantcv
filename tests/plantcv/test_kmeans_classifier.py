import pytest
import numpy as np
from plantcv.learn.train_kmeans import train_kmeans
from plantcv.plantcv.kmeans_classifier import mask_kmeans
from plantcv.plantcv.kmeans_classifier import predict_kmeans
from tests import synthetic


@pytest.fixture(scope="module")
def kmeans_models(tmp_path_factory):
    """Two-cluster models trained on uniform background and plant images (BGR and gray)."""
    models = {}
    for gray in (False, True):
        train_dir = tmp_path_factory.mktemp("kmeans_gray" if gray else "kmeans_rgb")
        img = synthetic.two_region_image(gray=gray)
        synthetic.write_images(train_dir, {"kmeans_train_1.png": np.full_like(img, img[0, 0]),
                                           "kmeans_train_2.png": np.full_like(img, img[0, -1])})
        models[gray] = str(train_dir / "kmeans_out.fit")
        train_kmeans(img_dir=str(train_dir), k=2, out_path=models[gray], prefix="kmeans_train", patch_size=3)
    return models


def _expected_labels(labeled_img):
    """Expected labels of the two-region image, taking each cluster's label from its region."""
    background, plant = labeled_img[0, 0], labeled_img[0, -1]
    # The image is symmetric about the boundary, so every patch is nearer the plant cluster exactly
    # when its center pixel is in the plant half (columns 30:60)
    expected = np.full(synthetic.TWO_REGION_SHAPE, background, dtype=np.uint8)
    expected[:, synthetic.TWO_REGION_SHAPE[1] // 2:] = plant
    return expected


@pytest.mark.parametrize("gray", [False, True])
def test_predict_kmeans_classifier(gray, kmeans_models):
    """Test for PlantCV."""
    labeled_img = predict_kmeans(img=synthetic.two_region_image(gray=gray), model_path=kmeans_models[gray],
                                 patch_size=3)
    assert labeled_img[0, 0] != labeled_img[0, -1]
    assert np.array_equal(labeled_img, _expected_labels(labeled_img))


def test_predict_kmeans_classifier_spectral(kmeans_models):
    """Test for PlantCV."""
    dummy_spectral = type("dummy_spectral", (object,), {"array_data": synthetic.two_region_image()})
    labeled_img = predict_kmeans(img=dummy_spectral, model_path=kmeans_models[False], patch_size=3,
                                 mode="spectral")
    assert labeled_img[0, 0] != labeled_img[0, -1]
    assert np.array_equal(labeled_img, _expected_labels(labeled_img))


def test_predict_kmeans_classifier_even_patch(tmp_path):
    """Test for PlantCV."""
    img = synthetic.two_region_image()
    background, plant = np.full_like(img, img[0, 0]), np.full_like(img, img[0, -1])
    synthetic.write_images(tmp_path, {"kmeans_train_1.png": background, "kmeans_train_2.png": plant})
    model = str(tmp_path / "kmeans_out.fit")
    train_kmeans(img_dir=str(tmp_path), k=2, out_path=model, prefix="kmeans_train", patch_size=4)
    # An even patch has no center pixel, so predict uniform images: one label each, same shape as the input
    background_labels = predict_kmeans(img=background, model_path=model, patch_size=4)
    plant_labels = predict_kmeans(img=plant, model_path=model, patch_size=4)
    assert background_labels.shape == plant_labels.shape == synthetic.TWO_REGION_SHAPE
    assert len(np.unique(background_labels)) == len(np.unique(plant_labels)) == 1
    assert background_labels[0, 0] != plant_labels[0, 0]


def _region_labels():
    """Labeled image of the synthetic plant: background 0, then stem, left leaf, right leaf, small object 1-4."""
    labeled_img = np.zeros(synthetic.PLANT_SHAPE, dtype=np.uint8)
    for value, mask in enumerate(synthetic.region_masks(), start=1):
        labeled_img[mask > 0] = value
    return labeled_img


def test_mask_kmeans():
    """Test for PlantCV."""
    mask_dict = mask_kmeans(labeled_img=_region_labels(), k=5)
    background = 255 - synthetic.plant_mask()
    for i, mask in enumerate([background] + synthetic.region_masks()):
        assert np.array_equal(mask_dict[str(i)], mask)


def test_mask_kmeans_gray(kmeans_models):
    """Test for PlantCV."""
    labeled_img = predict_kmeans(img=synthetic.two_region_image(gray=True), model_path=kmeans_models[True],
                                 patch_size=3)
    mask_dict = mask_kmeans(labeled_img=labeled_img, k=2)
    # The plant cluster's mask is the plant half; the background cluster's mask is the rest
    plant_half = np.zeros(synthetic.TWO_REGION_SHAPE, dtype=np.uint8)
    plant_half[:, synthetic.TWO_REGION_SHAPE[1] // 2:] = 255
    assert np.array_equal(mask_dict[str(labeled_img[0, -1])], plant_half)
    assert np.array_equal(mask_dict[str(labeled_img[0, 0])], 255 - plant_half)


def test_mask_kmeans_combo():
    """Test for PlantCV."""
    combo_mask = mask_kmeans(labeled_img=_region_labels(), k=5, cat_list=[1, 2])
    stem, left_leaf, _, _ = synthetic.region_masks()
    # Stem (240 px) and left leaf (280 px) do not overlap
    assert np.array_equal(combo_mask, stem | left_leaf)
    assert np.count_nonzero(combo_mask) == 520


def test_mask_kmeans_combo_gray(kmeans_models):
    """Test for PlantCV."""
    labeled_img = predict_kmeans(img=synthetic.two_region_image(gray=True), model_path=kmeans_models[True],
                                 patch_size=3)
    # Both clusters together cover the whole image
    combo_mask = mask_kmeans(labeled_img=labeled_img, k=2, cat_list=[0, 1])
    assert np.array_equal(combo_mask, np.full(synthetic.TWO_REGION_SHAPE, 255, dtype=np.uint8))
