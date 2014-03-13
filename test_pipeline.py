#!/usr/bin/python
import os, sys, traceback
import argparse

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Test a plantcv image processing pipeline with specific or randomly selected images.")
  parser.add_argument("-d", "--dir", help="Input directory containing images.", required=True)
  parser.add_argument("-p", "--pipeline", help="Pipeline script.", required=True)
  parser.add_argument("-r", "--random", help="Select a random set of images from the input directory", action="store_true")
  parser.add_argument("-n", "--num", help="Number of random images to test. Only used with -r. Default = 10", type=int, default=10)
  parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

### Main
def main():
  # Get options
  args = options()
  
  # Read input directory
  images = os.listdir(args.dir)
  for img in images:
    print img
  

if __name__ == '__main__':
  main()