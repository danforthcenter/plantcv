#!/usr/local/python3
import os
from os import listdir
from os.path import isfile,join
import sys, traceback
import cv2
import numpy as np
import argparse
import string
from plantcv import plantcv as pcv
from plantcv import learn as pc_learn
#from color_cluster_train import color_clustering_train

#from color_clustering_segmentation_selection_combined import color_clustering_segmentation


### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    #parser.add_argument("-p", "--pdfs", help="Naive Bayes PDF file.", required=True)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug",
                        help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.",
                        default=None)
    args = parser.parse_args()
    return args

#### Start of the Main/Customizable portion of the workflow.

### Main workflow
def main():
    # Get options
    args = options()


    pcv.params.debug = args.debug  # set debug mode
    pcv.params.debug_outdir = args.outdir  # set output directory

    # Read image
    img, path, filename = pcv.readimage(filename=args.image)

    # Convert RGB to HSV and extract the saturation channel
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

    # Threshold the saturation image
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=65, max_value=255, object_type='light')

    # Median Blur
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

    # Convert RGB to LAB and extract the Blue channel
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

    # Threshold the blue image
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')
    b_cnt = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')

    # Fill small objects
    # b_fill = pcv.fill(b_thresh, 10)

    # Join the thresholded saturation and blue-yellow images
    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)

    # Apply Mask (for VIS images, mask_color=white)
    masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')

##    edge=pcv.canny_edge_detect(masked)


##    if not os.path.exists("models"+"/"+filename.rstrip(".jpg")):
##        os.makedirs("models"+"/"+filename.rstrip(".jpg"))
   # color_clustering_train(masked, project_name=filename.rstrip(".jpg"),num_components=7,algorithm="Gaussian", sample_pixels=50, sample_pixel_file=filename.rstrip(".jpg")+"_alias_file_least12__.txt", remove_grays=True)


    #cropped=img[1656:3192, 256:3448]

    #masks = pcv.naive_bayes_classifier(rgb_img=cropped, pdf_file=args.pdfs)
    #colored_img = pcv.visualize.colorize_masks(masks=[masks['Leaf'], masks['Undesirables']],
    #                                           colors=['green','black'])


    #masked = pcv.apply_mask(img=cropped, mask=masks['Leaf'], mask_color='white')

    pc_learn.color_clustering_train(masked, remove_grays=True, num_components=4, algorithm="Gaussian", project_name="temp_testing_multi", sample_pixels=150, sample_pixel_file="temp_testing_multi_alias_file.txt")

   # _,submask=color_clustering_segmentation(masked, algorithm="Kmeans", alias_file="Temp_Multi_Alias_file.txt")



##
##    binary_img = pcv.median_blur(gray_img=submask[1], ksize=5)
##
##    pcv.fill(binary_img, 300)





##    ab_fill = pcv.fill_holes(bin_img=submask["LeavesOnly"])

##

##    pcv.print_image(out,"test.png")

##    _,submask=color_clustering_segmentation(img, project_name="TK003_Topview")
##
##
##    combined=cv2.add(submask[1],submask[3])
##
##    pcv.fill(combined, 20)
##
##    pcv.print_image(combined,"combined_submask.png")

    sys.exit()


##   im2, contours, hierarchy = cv2.findContours(submask["Diseases"], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
##
##    out = np.zeros(img.shape[:2], dtype="uint8")
##
##    for c in contours:
##        cv2.drawContours(out, [c], -1, 255, -1)
##
##    pcv.print_image(out,"contours.png")

    masked_of_original = pcv.apply_mask(img=img, mask=submask["LeavesOnly"], mask_color='white')

    LeafSize=np.count_nonzero(submask["LeavesOnly"])

    submask["Diseases"]=pcv.median_blur(gray_img=submask["Diseases"], ksize=5)

    submask["Diseases"]=pcv.fill(submask["Diseases"],130)



    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(submask["Diseases"], connectivity=8)

    sizes = stats[1:, -1]; nb_components = nb_components - 1

    min_size = LeafSize

    img2 = np.zeros((output.shape))


    for i in range(0, nb_components):
        if sizes[i] <= min_size:
            img2[output == i + 1] = 255

    # Threshold the saturation image
    s_thresh = pcv.threshold.binary(gray_img=img2, threshold=0, max_value=255, object_type='light')


    blurred = cv2.medianBlur(s_thresh, 9)
    _filter = cv2.bilateralFilter(s_thresh, 5, 75, 75)
    adap_thresh = cv2.adaptiveThreshold(_filter,
                                    255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV,
                                    21, 0)



    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

    dilate=cv2.dilate(adap_thresh, element, iterations=1)

    pcv.print_image(255-dilate,"hail.png")

    params = cv2.SimpleBlobDetector_Params()

##    params.minDistBetweenBlobs = 10
    params.filterByColor = True
    params.maxArea = 10000
##    params.minThreshold = 10
##    params.maxThreshold = 2000
    params.filterByArea = False
    params.minArea = 50
    params.filterByCircularity = False
    params.minCircularity = 0.3
    params.filterByConvexity = True
    params.minConvexity = 0
    params.filterByInertia = False
    params.minInertiaRatio = 0.1

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    h,w=submask["Diseases"].shape[0:2]

    base_size=h+20,w+20
    # make a 3 channel image for base which is slightly larger than target img
    base=np.zeros(base_size)
    cv2.rectangle(base,(0,0),(w+20,h+20),(0,0,0),30) # really thick white rectangle
    base[10:h+10,10:w+10]=submask["Diseases"] # this works

    base = pcv.threshold.binary(gray_img=base, threshold=0, max_value=255, object_type='light')

    keypoints = detector.detect(255 - s_thresh)

    blank = np.zeros((1, 1))

    black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    black[:] = (0, 0, 0)

    blobs = cv2.drawKeypoints(img, keypoints, blank, (0, 0, 255),
                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    pcv.print_image(submask["LeavesOnly"],"blobs.png")

    pcv.print_image(base,"borders.png")

    keypoints = detector.detect(255 - base)

    blank = np.zeros((1, 1))

    black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    black[:] = (0, 0, 0)

    blobs = cv2.drawKeypoints(img, keypoints, blank, (0, 0, 255),
                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    pcv.print_image(blobs,"blobs_afterborder.png")

    im2, contours, hierarchy = cv2.findContours(submask["LeavesOnly"], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    out = np.zeros(img.shape[:2], dtype="uint8")


    for c in contours:
        cv2.drawContours(out, [c], -1, 255, -1)
        for x in range(1,len(keypoints)):
            if (cv2.pointPolygonTest(c, (np.int(keypoints[x].pt[0]),np.int(keypoints[x].pt[1])), False))>=0:
                fmask = cv2.circle(black, (np.int(keypoints[x].pt[0]),np.int(keypoints[x].pt[1])), radius=np.int(keypoints[x].size)+10, color=(255), thickness=-1)

    graymask = cv2.cvtColor(fmask,cv2.COLOR_BGR2GRAY)

    (thresh, im_bw) = cv2.threshold(graymask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    masked = pcv.apply_mask(img=img, mask=im_bw, mask_color='white')

##    s = pcv.rgb2gray_hsv(rgb_img=masked, channel='s')
##
##    # Threshold the saturation image
##    s_thresh = pcv.threshold.binary(gray_img=s, threshold=0, max_value=255, object_type='light')
##
##    filled=pcv.fill_holes(s_thresh)
##
##
####
####    pcv.print_image(out,"Blob_again.png")
##
##    #graymask = cv2.cvtColor(out,cv2.COLOR_BGR2GRAY)
##
####    (thresh, im_bw) = cv2.threshold(out, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
##
##    masked = pcv.apply_mask(img=img, mask=im_bw, mask_color='white')

    pcv.print_image(masked,"final.png")


if __name__ == '__main__':
    main()
