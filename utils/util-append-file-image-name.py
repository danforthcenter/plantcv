#!/usr/bin/env python

import argparse
import sys, os
import re
import shutil

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Get file names to run FASTQC over")
  parser.add_argument("-d", "--directory", help="directory to run script over.")
  parser.add_argument("-o", "--outdir", help="out directory to move files to")
  args = parser.parse_args()
  return args

def append_img_name(directory,outdir):
    dirs=os.listdir(directory)
    
    dirname=str(directory)
    dirsplit=dirname.split('/')
    experiment=(dirsplit[-1])
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    for x in dirs:
        path=str(directory)+"/"+str(x)
        #print(path)
        if os.path.isdir(path) == True:
            files=os.listdir(path)
            outdirpath=str(outdir)+"/"+str(experiment)+"/"+str(x)
            os.makedirs(outdirpath)
            for i in files:
                filepath=str(path)+"/"+str(i)
                outfilepath=str(outdirpath)+"/"+str(experiment)+"_"+str(x)+"_"+str(i)
                shutil.copyfile(filepath,outfilepath)
                print(filepath)
                print(outfilepath)
            
    
### Main pipeline
def main():
  # Get options
  args = options()
  
  append_img_name(args.directory,args.outdir)
  

if __name__ == '__main__':
  main()
