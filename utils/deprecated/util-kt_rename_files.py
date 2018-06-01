#!/usr/bin/env python

import argparse
import sys, os
import sqlite3 as sq
from plantcv import plantcv as pcv
from shutil import copy
import datetime
import re

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
  parser.add_argument("-d", "--dir", help="directory of files to rename.")
  parser.add_argument("-c", "--camera", help="VIS_SV, VIS_TV.")
  parser.add_argument("-a", "--angle", help="0,90,180,270.")
  parser.add_argument("-z", "--zoom", help="zoom.")
  parser.add_argument("-e", "--date", help="startdate in epoch time", type=int)  
  parser.add_argument("-i", "--timeinterval", help="timeinterval in seconds.", type=int)
  parser.add_argument("-p", "--imagetype", help="jpg,png.")  
  args = parser.parse_args()
  return args


def read_dir(directory):
    for a,b,c in os.walk(directory):
        filenames=c
        path=a
    return filenames,path

def rename_move(filenames,path,camera,angle, zoom, date, timeinterval, imagetype):
    new_dir=str(path)+str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
    os.mkdir(new_dir)
    
    for i,x in enumerate(filenames):
        timeinterval_x=int(date)+int(((i+1)*timeinterval))
        new_time=datetime.datetime.fromtimestamp(int(timeinterval_x)).strftime('%Y-%m-%d %H_%M_%S')
        new_x=x.replace("_",".",2)
        new_name=str(new_x)+'-'+str(new_time)+'-'+str(camera)+'_'+str(angle)+'_'+str(zoom)+'.'+str(imagetype)
        copy(str(path)+ str(x),str(new_dir)+'/'+str(new_name))
        
        
### Main pipeline
def main():
  # Get options
  args = options()
  
  filenames,path=read_dir(args.dir)
  rename_move(filenames,path, args.camera, args.angle, args.zoom, args.date, args.timeinterval, args.imagetype)
  
if __name__ == '__main__':
  main()
#!/usr/bin/env python



