#!/usr/bin/env python

import argparse
import os
import re
import cv2


# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Resize images")
    parser.add_argument("-d", "--directory", help="directory to run script over.")
    parser.add_argument("-o", "--outdir", help="out directory to move files to")
    parser.add_argument("-r", "--resize_factor", help="out directory to move files to")
    args = parser.parse_args()
    return args


def image_resize(directory, outdir, resize_factor):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    files = os.listdir(directory)

    for x in files:
        if re.search("png$", x):
            outfile = os.path.join(outdir, str(x[:-4]) + "_downsized.png")
            orimg = str(directory) + str(x)
            img = cv2.imread(orimg, -1)
            thumbnail = cv2.resize(img, None, fx=float(resize_factor), fy=float(resize_factor),
                                   interpolation=cv2.INTER_AREA)
            cv2.imwrite(outfile, thumbnail)
        elif re.search("jpg$", x):
            outfile = os.path.join(outdir, str(x[:-4]) + "_downsized.jpg")
            orimg = str(directory) + str(x)
            img = cv2.imread(orimg, -1)
            thumbnail = cv2.resize(img, None, fx=float(resize_factor), fy=float(resize_factor),
                                   interpolation=cv2.INTER_AREA)
            cv2.imwrite(outfile, thumbnail)


# Main pipeline
def main():
    # Get options
    args = options()

    image_resize(args.directory, args.outdir, args.resize_factor)


if __name__ == '__main__':
    main()
