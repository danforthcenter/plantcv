from plantcv.plantcv.kmeans_classifier import mask_kmeans
from plantcv.plantcv.kmeans_classifier import predict_kmeans
from plantcv.plantcv import readimage


def test_kmeans_classifier(test_data):
    """Test for PlantCV."""
    input_dir = test_data.kmeans_classifier_dir
    input_dir_gray = test_data.kmeans_classifier_gray_dir
    labeled_img = predict_kmeans(img=input_dir+"/test_image.jpg", model_path=input_dir+"/kmeans_out.fit", patch_size=4)
    labeled_img_gray = predict_kmeans(img=input_dir_gray+"/test_image_gray.jpg",
                                      model_path=input_dir_gray+"/kmeans_out_gray.fit", patch_size=4)
    test_labeled, _, _ = readimage(input_dir+"/labeled_image.png")
    test_labeled_gray, _, _ = readimage(input_dir_gray+"/labeled_image_gray.png")
    assert (labeled_img == test_labeled).all()
    assert (labeled_img_gray == test_labeled_gray).all()

    mask_dict = mask_kmeans(labeled_img=labeled_img, k=4)
    mask_dict_gray = mask_kmeans(labeled_img=labeled_img_gray, k=4)
    for i in range(4):
        assert (readimage(input_dir+"/label_example_"+str(i)+".png")[0] == mask_dict[str(i)]).all()
    for i in range(4):
        assert (readimage(input_dir_gray+"/label_example_gray_"+str(i)+".png")[0] == mask_dict_gray[str(i)]).all()

    combo_mask = mask_kmeans(labeled_img=labeled_img, k=4, cat_list=[1, 2])
    combo_mask_gray = mask_kmeans(labeled_img=labeled_img_gray, k=4, cat_list=[1, 2])
    combo_example, _, _ = readimage(input_dir+"/combo_mask_example.png")
    combo_example_gray, _, _ = readimage(input_dir_gray+"/combo_mask_example_gray.png")
    assert (combo_mask == combo_example).all()
    assert (combo_mask_gray == combo_example_gray).all()
