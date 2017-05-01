#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import argparse
import datetime
from scipy import stats
import numpy as np
import cv2
import plantcv.learn


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.

    :return args: object -- parsed arguments
    :raises: IOError, KeyError
    """

    # Job start time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print("Starting run " + start_time + '\n', file=sys.stderr)

    methods = ["naive_bayes"]

    parser = argparse.ArgumentParser(description='PlantCV machine learning training script.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--imgdir", help='Input directory containing images.', required=True)
    parser.add_argument("-b", "--maskdir", help="Input directory containing black/white masks.", required=True)
    parser.add_argument("-m", "--method", help="Learning method. Available methods: " + ", ".join(map(str, methods)),
                        required=True)
    parser.add_argument("-o", "--outfile", help="Trained classifier output filename.", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.imgdir):
        raise IOError("Directory does not exist: {0}".format(args.imgdir))
    if not os.path.exists(args.maskdir):
        raise IOError("Directory does not exist: {0}".format(args.maskdir))
    if args.method not in methods:
        raise KeyError("Method is not supported: {0}".format(args.method))

    return args


###########################################


# Main
###########################################
def main():
    """Main program.

    """

    # Parse command-line options
    args = options()

    if args.method == "naive_bayes":
        plantcv.learn.naive_bayes(args.imgdir, args.maskdir, args.outfile)


###########################################


if __name__ == '__main__':
    main()
