#!/usr/bin/env python
import argparse
import sys, os
import sqlite3 as sq
import plantcv as pcv
from shutil import copy
import datetime
import re

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
  parser.add_argument("-d", "--database", help="SQLite database file from plantcv.")
  parser.add_argument("-c", "--csv", help="PhenoFront CSV file.")
  parser.add_argument("-r", "--random", help="number of random images you would like", type=int, required=False)
  parser.add_argument("-o", "--outdir", help="Output directory.", required=True)
  parser.add_argument("-s", "--camera", help= "vis_sv, vis_tv, nir_sv, nir_tv, flu_tv", required=True)
  parser.add_argument("-t", "--type", help="Image format type.", required=True)
  args = parser.parse_args()
  return args

### Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

### Grab Random Image Ids From Database
def grab_random(database,random, camera, outdir, type):
  # Does the database exist?
  if not os.path.exists(database):
    pcv.fatal_error("The database file " + str(database) + " does not exist");
  
  # Open a connection
  try:
    connect=sq.connect(database)
  except sq.Error, e:
    print("Error %s:" % e.args[0])
    
  # Replace the row_factory result constructor with a dictionary constructor
  connect.row_factory = dict_factory
  # Change the text output format from unicode to UTF-8
  connect.text_factory=str

   # Database handler
  db = connect.cursor()
  imageid_list=[]
  num=random
  print num
  list_random= db.execute('select * from snapshots where camera=? order by random() limit ?' , (camera,num,))
  for i, x in enumerate(list_random):
    imgid=x['image_id']
    imageid_list.append(imgid)
  
  print imageid_list
  
  for i,t in enumerate(imageid_list):
    get_image=db.execute('select * from snapshots where image_id=?',(t,))
    for a, data in enumerate(get_image):
      img_name = outdir + '/' + data['plant_id'] + '_' + data['camera'] + '_' + str(data['frame']) + '_z' + str(data['zoom']) + '_h' + str(data['lifter']) + '_' + str(t) + '.' + type
      copy(data['image_path'], img_name)
    print "copying"
    print img_name   
        

### Main pipeline
def main():
  # Get options
  args = options()
  

  grab_random(args.database, args.random, args.camera, args.outdir, args.type)


if __name__ == '__main__':
  main()
