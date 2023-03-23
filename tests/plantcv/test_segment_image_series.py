import os
import cv2
import numpy as np
from plantcv.plantcv import segment_image_series
from plantcv.plantcv.roi import multi
from plantcv.plantcv import params


def test_plantcv_segment_image_series(tmpdir):
    """Test for PlantCV."""
    # parameters for the synthetic image series to generate
    H, W, C = 32, 32, 3
    FRAMES = 10
    RGB_VAL = [50, 150, 50]
    OBJ1_COORDS = [10, 10]
    SPACING = (10, 10)
    OBJ2_COORDS = [OBJ1_COORDS[0]+SPACING[0], OBJ1_COORDS[1]+SPACING[1]]
    OBJ_SIZE = 4

    rng = np.random.default_rng(0)
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    cache_img_dir = os.path.join(cache_dir, 'segment_image_series_images')
    os.mkdir(cache_img_dir)
    cache_mask_dir = os.path.join(cache_dir, 'segment_image_series_masks')
    os.mkdir(cache_mask_dir)
    cache_out_dir = os.path.join(cache_dir, 'segment_image_series_out')
    os.mkdir(cache_out_dir)

    imgs_paths = []
    masks_paths = []

    # generate image series
    obj1_init = np.array(OBJ1_COORDS)
    obj2_init = np.array(OBJ2_COORDS)
    for i in range(FRAMES):
        img = np.zeros((H, W, C), dtype=np.uint8)

        obj1 = obj1_init + rng.integers(low=-1, high=1, size=2)
        img[obj1[0]:obj1[0]+OBJ_SIZE, obj1[1]:obj1[1]+OBJ_SIZE, :] = RGB_VAL
        obj2 = obj2_init + rng.integers(low=-1, high=1, size=2)
        img[obj2[0]:obj2[0]+OBJ_SIZE, obj2[1]:obj2[1]+OBJ_SIZE, :] = RGB_VAL

        img_path = os.path.join(cache_img_dir, f"{i}.png")
        mask_path = os.path.join(cache_mask_dir, f"{i}_mask.png")

        cv2.imwrite(img_path, img)
        cv2.imwrite(mask_path, 255*(img != 0).astype(np.uint8))

        imgs_paths.append(img_path)
        masks_paths.append(mask_path)

    # pcv.params.color_sequence = 'random'

    roi_objects = multi(img=img, coord=(OBJ1_COORDS[0], OBJ1_COORDS[1]),
                        radius=OBJ_SIZE-2, spacing=SPACING, nrows=2, ncols=2)
    rois, _ = roi_objects.contours, roi_objects.hierarchy
    valid_rois = [rois[0], rois[3]]

    # test that the function detects the two objects and propagates the labels
    # to the last frame
    markers = segment_image_series(imgs_paths, masks_paths, rois=valid_rois, save_labels=True, ksize=3)

    nb_obj = np.unique(markers[:, :, FRAMES-1]).size - 1

    assert nb_obj == 2
