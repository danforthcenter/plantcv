#!/usr/bin/env python

import argparse
import numpy as np
import sys, os
import sqlite3 as sq
from plantcv import plantcv as pcv
from shutil import copy
import datetime
import re

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Get images from an SQLite database and some input information")
  parser.add_argument("-d", "--database", help="SQLite database file from plantcv.")
  parser.add_argument("-f", "--file", help="text file, tab seperated, containing plant IDs and other information.", required=True)
  parser.add_argument("-o", "--outdir", help="Output directory.", required=False)
  parser.add_argument("--vis", help="Images are class VIS.", action='store_true')
  parser.add_argument("--nir", help="Images are class NIR.", action='store_true')
  parser.add_argument("--flu", help="Images are class FLU.", action='store_true')
  parser.add_argument("-t", "--type", help="Image format type.", required=True)
  args = parser.parse_args()
  return args


### Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
  
  
### Get images with more information
def dict_plant_info(infile):  
  table=np.genfromtxt(infile, dtype='str', delimiter='\t')
  table1=np.asarray(table)
  
  query=[]
  
  header=table[0].tolist()
  tablenohead=table[1:]
  y,x=tablenohead.shape
  columncount=list(range(0,x))
  split_table=np.vsplit(tablenohead,y)
  split_table= [l[0] for l in split_table]
  
  for row in split_table:
    where=[]
    col=np.hsplit(row,x)
    col=[l[0] for l in col]
    for i,h in enumerate(columncount):
      where.append(str(header[i])+'='+"'"+str(col[i]+"'"))
    where_and=' and '.join(map(str,where))
    query.append(where_and)
  return query

### Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

### Database image lookup method
def db_lookup(database, outdir, query, type, vis=False, nir=False, flu=False):
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
  
  for row in query:
    print row
    
    query1='select * from snapshots where ' + str(row)
    print query1
    for row in (db.execute(query1)):
      dt = datetime.datetime.fromtimestamp(row['datetime']).strftime('%Y-%m-%d %H:%M:%S')
      if (vis):
        if (row['camera'] == 'vis_sv' or row['camera'] == 'vis_tv'):
          img_name = outdir + '/' + row['plant_id'] + '_' + row['camera'] + '_' + str(row['frame']) + '_z' + str(row['zoom']) + '_h' + str(row['lifter']) + '_' + dt + '.' + type
          copy(row['image_path'], img_name)
          #print(args.outdir + '/' + row['plant_id'])
      if (nir):
        if (row['camera'] == 'nir_sv' or row['camera'] == 'nir_tv'):
          img_name = outdir + '/' + row['plant_id'] + '_' + row['camera'] + '_' + str(row['frame']) + '_z' + str(row['zoom']) + '_h' + str(row['lifter']) + '_' + dt + '.' + type
          copy(row['image_path'], img_name)
      if (flu):
        if (row['camera'] == 'flu_tv'):
          images = row['image_path'].split(',')
          for i in enumerate(images):
            img_name = outdir + '/' + row['plant_id'] + '_' + row['camera'] + '_' + str(row['frame']) + '_z' + str(row['zoom']) + '_h' + str(row['lifter']) + '_' + str(i) + '_' + dt + '.' + type
            copy(images[i], outdir)

### Main pipeline
def main():
  # Get options
  args = options()
  
  query=dict_plant_info(args.file)
  db_lookup(args.database, args.outdir, query, args.type, args.vis, args.nir, args.flu)
  

if __name__ == '__main__':
  main()