#!/usr/bin/env python

import os
import shutil
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


# ##############################
# Clean up test files
# ##############################
def teardown_function():
    shutil.rmtree(TEST_TMPDIR)
