from plantcv import plantcv as pcv
from pcv.kmeans_classifier import mask_kmeans
from pcv.kmeans_classifier import predict_kmeans


def test_kmeans_classifier(test_data):
    """Test for PlantCV."""
    input_dir = test_data.kmeans_classifier_dir
    labeled_img = predict_kmeans(img=input_dir+"/test_image.jpg", model_path=input_dir+"/kmeans_out.fit", patch_size=5)
    test_labeled, _, _ = pcv.readimage(input_dir+"/labeled_image.png")
    assert (labeled_img == test_labeled).all()
    
    mask_dict = mask_kmeans(labeled_img=labeled_img, K=4, patch_size=5)
    for i in range(4):
        assert (pcv.readimage(input_dir+"/label_example_"+str(i)+".png")[0] == mask_dict[str(i)]).all()

    combo_mask = mask_kmeans(labeled_img=labeled_img, K=4, patch_size=5, cat_list=[1,2])
    combo_example, _, _ = pcv.readimage(input_dir+"/combo_mask_example.png")
    assert (combo_mask == combo_example).all()
    