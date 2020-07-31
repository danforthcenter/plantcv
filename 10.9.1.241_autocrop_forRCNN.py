import os
import sys
from plantcv import plantcv as pcv
import cv2
import numpy as np
import argparse

### Parse command-line arguments
# def options():
#     parser = argparse.ArgumentParser(description="Imaging processing with opencv")
#     parser.add_argument("-r", "--result", help="result file.", required=False)
#     parser.add_argument("-i", "--image", help="Input image file.", required=True)
#     parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
#     parser.add_argument("-n", "--names", help="path to txt file with names of genotypes to split images into", required =False)
#     parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action=None)
#     args = parser.parse_args()
#     return args

def main():

    # Get options
    #args = options()

    # Set variables
    #pcv.params.debug = args.debug     # Replace the hard-coded debug with the debug flag


    #import image
    img, path, img_filename = pcv.readimage(filename = "/Users/acasto/Documents/plantcv_local_test/auto_crop/10.9.1.241_pos-165-003-020_2019-10-31-14-05.jpg")
    filename = img_filename
    outdir = "Users/acasto/Documents/plantcv_local_test/auto_crop/"

    #check if the image is a night image
    if np.average(img) < 20:
        pcv.fatal_error("Night Image")
    else:
        pass

    #check if the image is not stupidly small
    if np.shape(img)[0] < 1000:
        pcv.fatal_error("bad zoom")
    else:
        pass

    #rotate the image to straighten the grid
    #rotate_img = pcv.rotate(img, -1, True)

    #white balance
    img1 = pcv.white_balance(img = img, roi=(350,650,30,30))

    #segmenting plants
    a = pcv.rgb2gray_lab(rgb_img=img1, channel="a")
    img_binary = pcv.threshold.binary(gray_img=a, threshold=120, max_value=255, object_type='dark')

    #fill small holes
    fill_image = pcv.fill(bin_img=img_binary, size=300)

    #dilate
    dilated = pcv.dilate(gray_img=fill_image, ksize=2, i=1)

    #find objects
    id_objects, obj_hierarchy = pcv.find_objects(img=img1, mask=dilated)

    #Define the ROI
    #roi_contour, roi_hierarchy = pcv.roi.rectangle(img=img1, x=500, y=5, h=2400, w=1900)

    #Keep objects within the ROI
#     roi_objects, roi_obj_hierarchy, kept_mask, obj_area = pcv.roi_objects(img=img1, roi_contour=roi_contour,
#                                                                             roi_hierarchy=roi_hierarchy,
#                                                                             object_contour=id_objects,
#                                                                             obj_hierarchy=obj_hierarchy,
#                                                                             roi_type='partial')

    masked_image = pcv.apply_mask(img=img1, mask= dilated, mask_color='black')

    #defining multiple ROIs
    rois1, roi_hierarchy1 = pcv.roi.multi(img=img1, coord=(1050,260), radius=150, spacing=(470,400), nrows=6, ncols=4)

    #shape analysis
    # The result file should exist if plantcv-workflow.py was run
    # if os.path.exists(args.result):
    #     # Open the result file
    #     results = open(args.result, "r")
    #     # The result file would have image metadata in it from plantcv-workflow.py, read it into memory
    #     metadata = results.read()
    #     # Close the file
    #     results.close()
    #     # Delete the file, we will create new ones
    #     os.remove(args.result)
    # else:
    #     # If the file did not exist (for testing), initialize metadata as an empty string
    #     metadata = "{}"

    for i in range(0, len(rois1)):
        roi = rois1[i]
        hierarchy = roi_hierarchy1[i]
        # Find objects
        filtered_contours, filtered_hierarchy, filtered_mask, filtered_area = pcv.roi_objects(img=img1, roi_type="partial",
                                                                                              roi_contour=roi,
                                                                                              roi_hierarchy=hierarchy,
                                                                                              object_contour=id_objects,
                                                                                              obj_hierarchy=obj_hierarchy)
        # Combine objects together in each plant
        plant_contour, plant_mask = pcv.object_composition(img=img1, contours=filtered_contours,
                                                           hierarchy=filtered_hierarchy)

        if plant_contour is None:
            failed_plant = cv2.drawContours(np.copy(img), roi, -1, (255, 0, 0), 9)
            filename_failed = img_filename + "_" + str(i)+".jpg"
            pcv.print_image(img=failed_plant, filename=os.path.join(outdir, "contour_none", filename_failed))
        else:
            analysis_images = pcv.analyze_object(img=img1, obj=plant_contour, mask=plant_mask)

        if pcv.outputs.observations['area']['value'] < 80000:
            crop_img = pcv.auto_crop(img = img1, obj= plant_contour, padding_x=(50,100),
                                     padding_y=(50,100), color='BLACK')
            pcv.print_image(img = crop_img, filename = os.path.join(outdir,
                                                                    filename[:-4] + "_crop-img" + str(i) + ".jpg"))
        else:
            crop_bigboi = pcv.auto_crop(img = masked_image, obj= plant_contour, padding_x=100, padding_y=100, color='black')
        # Clear the measurements stored globally into the Ouptuts class
        pcv.outputs.clear()

if __name__ == '__main__':
    main()
