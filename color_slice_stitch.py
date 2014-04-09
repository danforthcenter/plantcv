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
  #parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
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
  
  slice_stack1=[]
  slice_stack2=[]
  slice_stack3=[]
  
  for filename in os.listdir(args.directory):
    #re.sub('\s','_', filename)
    line1=cv2.imread((args.directory+'/'+filename))
    split1, split2, split3=np.dsplit(line1,3)
    #stacked_1=np.hstack((split1,split1,split1,split1,split1,split1,split1,split1,split1,split1))
    #stacked_2=np.hstack((split2,split2,split2,split2,split2,split2,split2,split2,split2,split2))
    #stacked_3=np.hstack((split3,split3,split3,split3,split3,split3,split3,split3,split3,split3))
    
    print np.shape(split1)
    slice_stack1.append(split1)
    slice_stack2.append(split2)
    slice_stack3.append(split3)
  
  print np.shape(slice_stack1)
  print np.shape(slice_stack2)
  print np.shape(slice_stack3)
  

if __name__ == '__main__':
  main()
        


    
