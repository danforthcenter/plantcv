#!/usr/bin/env python

import sys, traceback
import os
import re
import sqlite3
import distutils.core
import cv2
import numpy as np
import argparse
import string
import plantcv as pcv
import visualize_plantcv_results as avr

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Sitching and Ordering Image Slices")
  parser.add_argument("-d", "--database", help="Database to query.", required=True)
  parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
  #parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

### Main pipeline
def main():
  # Get options
  args = options()

  img_file_dir =avr.d3_color_output(args.database,args.outdir,'Dp1AA','vis','vis_sv','rgb','on','off','yes','yes','all')
  #img_file_dir='/home/mgehan/LemnaTec/out_folder/slice_figs_and_images_04-21-2014_16:59:07/'
  #avr.cat_fig(args.outdir,img_file_dir)

if __name__ == '__main__':
  main()
        


    
