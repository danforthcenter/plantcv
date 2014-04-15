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
import analyze_vis_results as avr

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

  time_array, id_unique, folder_path=avr.slice_stitch(args.database, args.outdir, 'vis_sv', 'off')
  avr.slice_figure(folder_path)
  
if __name__ == '__main__':
  main()
        


    
