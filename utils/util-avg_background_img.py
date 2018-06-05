#!/usr/bin/env python

import argparse
import numpy as np
import os
from plantcv import plantcv as pcv


# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Get images from an SQLite database and some input information")
    parser.add_argument("-d", "--directory", help="path to directory of images to average.")
    parser.add_argument("-o", "--outdir", help="Output directory.", required=False)
    args = parser.parse_args()
    return args


# Functions
def average_all_img(directory, outdir):
    allfiles = os.listdir(directory)
    
    path = str(directory)
    
    allpaths = []
    
    for files in allfiles:
        p = path + str(files)
        allpaths.append(p)
    
    img, path, filename = pcv.readimage(allpaths[0])
    n = len(allpaths)

    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
        arr = np.zeros((ix, iy, iz), np.float)
    else:
        ix, iy = np.shape(img)
        arr = np.zeros((ix, iy), np.float)

    # Build up average pixel intensities, casting each image as an array of floats
    for i, paths in enumerate(allpaths):
        img, path, filename = pcv.readimage(allpaths[i])
        imarr = np.array(img, dtype=np.float)
        arr = arr + imarr / n

    # Round values in array and cast as 8-bit integer
    arr = np.array(np.round(arr), dtype=np.uint8)

    pcv.print_image(arr, (str(outdir)+"average_"+str(allfiles[0])))


# Main pipeline
def main():
    # Get options
    args = options()

    average_all_img(args.directory, args.outdir)


if __name__ == '__main__':
    main()
