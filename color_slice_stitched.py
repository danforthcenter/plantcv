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

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Sitching and Ordering Image Slices")
  parser.add_argument("-d", "--directory", help="Input image file directory.", required=True)
  parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
  #parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

### Main pipeline
def main():
  # Get options
  args = options()

  #for filename in os.listdir(args.directory):
  #  if re.search("rgb_norm_slice\.png$",filename):
  #     fromDirectory = str(args.directory)+'/'+str(filename)
  #     toDirectory = "/home/mgehan/LemnaTec/colorslices/"+str(filename)
  #     distutils.file_util.copy_file(fromDirectory, toDirectory)
  #  else:
  #    pass

  ch1=[]
  ch2=[]
  ch3=[]
  
  for filename in os.listdir(args.directory):
    #re.sub('\s','_', filename)
    line1=cv2.imread((args.directory+'/'+filename))
    split1, split2, split3=np.dsplit(line1,3)
    split1_f=split1.flatten()
    split2_f=split2.flatten()
    split3_f=split3.flatten()
    stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f))
    stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f))
    stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f)) 
    stacked_1t=np.transpose(stacked_1)
    stacked_2t=np.transpose(stacked_2)
    stacked_3t=np.transpose(stacked_3)
    ch1.extend(stacked_1t)
    ch2.extend(stacked_2t)
    ch3.extend(stacked_3t)
  
  color_cat=np.dstack((ch1,ch2,ch3))
  pcv.print_image(color_cat,"color_slice_joined_img.png")

if __name__ == '__main__':
  main()
        


    
