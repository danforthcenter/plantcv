#!/usr/bin/env python

import pytest
import os
import shutil
import numpy as np
import cv2
from plantcv import plantcv as pcv
# Import matplotlib and use a null Template to block plotting to screen
# This will let us test debug = "plot"
import matplotlib

TEST_TMPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache")


# ##########################
# Tests setup function
# ##########################
def setup_function():
    if not os.path.exists(TEST_TMPDIR):
        os.mkdir(TEST_TMPDIR)


# ####################################################################################################################
# ########################################### PLANTCV MAIN PACKAGE ###################################################
matplotlib.use('Template')

TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TEST_INPUT_BINARY = "input_binary_img.png"
TEST_INPUT_SKELETON = 'input_skeleton.png'
TEST_INPUT_SKELETON_PRUNED = 'input_pruned_skeleton.png'
TEST_SKELETON_OBJECTS = "skeleton_objects.npz"
TEST_SKELETON_HIERARCHIES = "skeleton_hierarchies.npz"


# ####################################
# Tests for the morphology subpackage
# ####################################
def test_plantcv_morphology_segment_curvature():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_curvature(segmented_img, seg_objects)
    assert len(pcv.outputs.observations['default']['segment_curvature']['value']) == 22


def test_plantcv_morphology_check_cycles():
    # Clear previous outputs
    pcv.outputs.clear()
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    pcv.params.debug = None
    _ = pcv.morphology.check_cycles(mask)
    assert pcv.outputs.observations['default']['num_cycles']['value'] == 1


def test_plantcv_morphology_find_branch_pts():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    branches = pcv.morphology.find_branch_pts(skel_img=skeleton, mask=mask, label="prefix")
    assert np.sum(branches) == 9435


def test_plantcv_morphology_find_branch_pts_no_mask():
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    branches = pcv.morphology.find_branch_pts(skel_img=skeleton)
    assert np.sum(branches) == 9435


def test_plantcv_morphology_find_tips():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    tips = pcv.morphology.find_tips(skel_img=skeleton, mask=mask, label="prefix")
    assert np.sum(tips) == 9435


def test_plantcv_morphology_find_tips_no_mask():
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    tips = pcv.morphology.find_tips(skel_img=skeleton)
    assert np.sum(tips) == 9435


def test_plantcv_morphology_prune():
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    pruned_img, _, _ = pcv.morphology.prune(skel_img=skeleton, size=1, mask=skeleton)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_plantcv_morphology_prune_no_mask():
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    pruned_img, _, _ = pcv.morphology.prune(skel_img=skeleton, size=3)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_plantcv_morphology_prune_size0():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned_img, _, _ = pcv.morphology.prune(skel_img=skeleton, size=0)
    assert np.sum(pruned_img) == np.sum(skeleton)


def test_plantcv_morphology_iterative_prune():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_pruned")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned_img = pcv.morphology._iterative_prune(skel_img=skeleton, size=3)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_plantcv_morphology_segment_skeleton():
    pcv.params.debug = None
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    _ = pcv.morphology.segment_skeleton(skel_img=skeleton, mask=mask)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    assert len(segment_objects) == 73


def test_plantcv_morphology_fill_segments():
    # Clear previous outputs
    pcv.outputs.clear()
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_dic = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS))
    obj = []
    for key, val in obj_dic.items():
        obj.append(val)
    pcv.params.debug = None
    _ = pcv.morphology.fill_segments(mask, obj)
    tests = [pcv.outputs.observations['default']['segment_area']['value'][42] == 5529,
             pcv.outputs.observations['default']['segment_area']['value'][20] == 5057,
             pcv.outputs.observations['default']['segment_area']['value'][49] == 3323]
    assert all(tests)


def test_plantcv_morphology_fill_segments_with_stem():
    # Clear previous outputs
    pcv.outputs.clear()
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_dic = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS))
    obj = []
    for key, val in obj_dic.items():
        obj.append(val)

    stem_obj = obj[0:4]
    pcv.params.debug = None
    _ = pcv.morphology.fill_segments(mask, obj, stem_obj)
    num_objects = len(pcv.outputs.observations['default']['leaf_area']['value'])
    assert num_objects == 69


def test_plantcv_morphology_segment_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    pcv.params.debug = None
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_angle(segmented_img=segmented_img, objects=segment_objects)
    assert len(pcv.outputs.observations['default']['segment_angle']['value']) == 22


def test_plantcv_morphology_segment_angle_overflow():
    # Clear previous outputs
    pcv.outputs.clear()
    # Don't prune, would usually give overflow error without extra if statement in segment_angle
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_angle(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_angle']['value']) == 73


def test_plantcv_morphology_segment_euclidean_length():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_euclidean_length(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_eu_length']['value']) == 22


def test_plantcv_morphology_segment_euclidean_length_bad_input():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skel = pcv.morphology.skeletonize(mask=mask)
    pcv.params.debug = None
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    with pytest.raises(RuntimeError):
        _ = pcv.morphology.segment_euclidean_length(segmented_img, segment_objects)


def test_plantcv_morphology_segment_path_length():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_path_length(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_path_length']['value']) == 22


def test_plantcv_morphology_skeletonize():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    input_skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    skeleton = pcv.morphology.skeletonize(mask=mask)
    arr = np.array(skeleton == input_skeleton)
    assert arr.all()


def test_plantcv_morphology_segment_sort():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(skeleton, seg_objects, mask=skeleton)
    assert len(leaf_obj) == 36


def test_plantcv_morphology_segment_sort_no_mask():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(skeleton, seg_objects)
    assert len(leaf_obj) == 36


def test_plantcv_morphology_segment_tangent_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    objects = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS), encoding="latin1")
    objs = [objects[arr_n] for arr_n in objects]
    _ = pcv.morphology.segment_tangent_angle(skel, objs, 2)
    assert len(pcv.outputs.observations['default']['segment_tangent_angle']['value']) == 73


def test_plantcv_morphology_segment_id():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    objects = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS), encoding="latin1")
    objs = [objects[arr_n] for arr_n in objects]
    _, labeled_img = pcv.morphology.segment_id(skel, objs, mask=skel)
    assert np.sum(labeled_img) > np.sum(skel)


def test_plantcv_morphology_segment_id_no_mask():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    objects = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS), encoding="latin1")
    objs = [objects[arr_n] for arr_n in objects]
    _, labeled_img = pcv.morphology.segment_id(skel, objs)
    assert np.sum(labeled_img) > np.sum(skel)


def test_plantcv_morphology_segment_insertion_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=6)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 3, label="prefix")
    _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 10)
    assert pcv.outputs.observations['default']['segment_insertion_angle']['value'][:6] == ['NA', 'NA', 'NA',
                                                                                           24.956918822001636,
                                                                                           50.7313343343401,
                                                                                           56.427712102130734]


def test_plantcv_morphology_segment_insertion_angle_bad_stem():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=5)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    stem_obj = [leaf_obj[0], leaf_obj[10]]
    with pytest.raises(RuntimeError):
        _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 10)


def test_plantcv_morphology_segment_combine():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    # Test with list of IDs input
    _, new_objects = pcv.morphology.segment_combine([0, 1], seg_objects, skel)
    assert len(new_objects) + 1 == len(seg_objects)


def test_plantcv_morphology_segment_combine_lists():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    # Test with list of lists input
    _, new_objects = pcv.morphology.segment_combine([[0, 1, 2], [3, 4]], seg_objects, skel)
    assert len(new_objects) + 3 == len(seg_objects)


def test_plantcv_morphology_segment_combine_bad_input():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    with pytest.raises(RuntimeError):
        _, new_objects = pcv.morphology.segment_combine([0.5, 1.5], seg_objects, skel)


def test_plantcv_morphology_analyze_stem():
    pcv.params.debug = "plot"
    # Clear previous outputs
    pcv.outputs.clear()
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, segmented_img, _ = pcv.morphology.prune(skel_img=skeleton, size=6)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    _ = pcv.morphology.analyze_stem(rgb_img=segmented_img, stem_objects=stem_obj)
    assert pcv.outputs.observations['default']['stem_angle']['value'] == -12.531776428222656


def test_plantcv_morphology_analyze_stem_bad_angle():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=5)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    _, _ = pcv.morphology.segment_sort(pruned, seg_objects)
    # print([stem_obj[3]])
    # stem_obj = [stem_obj[3]]
    stem_obj = [[[[1116, 1728]], [[1116, 1]]]]
    pcv.params.debug = "plot"
    _ = pcv.morphology.analyze_stem(rgb_img=segmented_img, stem_objects=stem_obj)
    assert pcv.outputs.observations['default']['stem_angle']['value'] == 22877334.0


# ##############################
# Clean up test files
# ##############################
def teardown_function():
    shutil.rmtree(TEST_TMPDIR)
