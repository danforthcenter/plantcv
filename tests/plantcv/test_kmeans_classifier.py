import cv2
import os
from plantcv.plantcv.kmeans_classifier import mask_kmeans
from plantcv.plantcv.kmeans_classifier import predict_kmeans


def test_predict_kmeans_classifier(test_data):
    """Test for PlantCV."""
    input_dir = test_data.kmeans_classifier_dir
    rgb_img = cv2.imread(os.path.join(input_dir, "test_image.jpg"), -1)
    labeled_img = predict_kmeans(img=rgb_img, model_path=os.path.join(input_dir, "kmeans_out.fit"), patch_size=4)
    test_labeled = cv2.imread(os.path.join(input_dir, "labeled_image.png"), -1)
    assert (labeled_img == test_labeled).all()


def test_predict_kmeans_classifier_gray(test_data):
    """Test for PlantCV."""
    input_dir_gray = test_data.kmeans_classifier_gray_dir
    gray_img = cv2.imread(os.path.join(input_dir_gray, "test_image_gray.jpg"), -1)
    labeled_img_gray = predict_kmeans(img=gray_img, model_path=os.path.join(input_dir_gray, "kmeans_out_gray.fit"),
                                      patch_size=4)
    test_labeled_gray = cv2.imread(os.path.join(input_dir_gray, "labeled_image_gray.png"), -1)
    assert (labeled_img_gray == test_labeled_gray).all()


def test_mask_kmeans(test_data):
    """Test for PlantCV."""
    input_dir = test_data.kmeans_classifier_dir
    labeled_img = cv2.imread(os.path.join(input_dir, "labeled_image.png"), -1)
    mask_dict = mask_kmeans(labeled_img=labeled_img, k=4)
    for i in range(4):
        test_labeled = cv2.imread(os.path.join(input_dir, f"label_example_{i}.png"), -1)
        assert (test_labeled == mask_dict[str(i)]).all()


def test_mask_kmeans_gray(test_data):
    """Test for PlantCV."""
    input_dir_gray = test_data.kmeans_classifier_gray_dir
    labeled_img_gray = cv2.imread(os.path.join(input_dir_gray, "labeled_image_gray.png"), -1)
    mask_dict_gray = mask_kmeans(labeled_img=labeled_img_gray, k=4)
    for i in range(4):
        test_labeled_gray = cv2.imread(os.path.join(input_dir_gray, f"label_example_gray_{i}.png"), -1)
        assert (test_labeled_gray == mask_dict_gray[str(i)]).all()


def test_mask_kmeans_combo(test_data):
    """Test for PlantCV."""
    input_dir = test_data.kmeans_classifier_dir
    labeled_img = cv2.imread(os.path.join(input_dir, "labeled_image.png"), -1)
    combo_mask = mask_kmeans(labeled_img=labeled_img, k=4, cat_list=[1, 2])
    combo_example = cv2.imread(os.path.join(input_dir, "combo_mask_example.png"), -1)
    assert (combo_mask == combo_example).all()


def test_mask_kmeans_combo_gray(test_data):
    """Test for PlantCV."""
    input_dir_gray = test_data.kmeans_classifier_gray_dir
    labeled_img_gray = cv2.imread(os.path.join(input_dir_gray, "labeled_image_gray.png"), -1)
    combo_mask_gray = mask_kmeans(labeled_img=labeled_img_gray, k=4, cat_list=[1, 2])
    combo_example_gray = cv2.imread(os.path.join(input_dir_gray, "combo_mask_example_gray.png"), -1)
    assert (combo_mask_gray == combo_example_gray).all()
