#!/usr/bin/env python

import sys, traceback
import os
import re
import cv2
import numpy as np
import argparse
import string
import plantcv as pcv

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Sitching and Ordering Image Slices")
  parser.add_argument("-d", "--directory", help="Input image file directory.", required=True)
  #parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
  #parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

### Main pipeline
def main():
  # Get options
  args = options()

  for filename in os.listdir(args.directory):
    if re.search("rgb_norm_slice\.png$",filename):
      print filename

if __name__ == '__main__':
  main()
        


    
