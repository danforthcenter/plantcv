#!/usr/bin/env python
import argparse
import sys, os
import sqlite3 as sq
from plantcv import plantcv as pcv
import math
import shutil
import numpy as np
from numpy import genfromtxt

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
  parser.add_argument("-f", "--folder", help="txt file of folder names", required=True)
  parser.add_argument("-i", "--imgfolder", help="imgfolder name", required=True)
  parser.add_argument("-o", "--outdir", help="new folder destination", required=True)
  args = parser.parse_args()
  return args


def main():
  
  args = options()
  path=os.getcwd()
  #folders=open(args.folder, 'r')
  #for l in folders:
  #  fname=l.replace("\n", "")
  #  source=str(path)+"/"+str(args.imgfolder)+"/"+str(fname)
  #  destination=str(path)+"/"+str(args.outdir)
  #  shutil.move(source, destination)
  
  snapshots=str(path)+"/"+str(args.imgfolder)+"/SnapshotInfo.csv"
  #snapshot_data = genfromtxt(snapshots, delimiter=',')
  regex="^.*B*.*$"
  select=np.fromregex(snapshots,regex)
  print snapshot_data
  
if __name__ == '__main__':
  main()
